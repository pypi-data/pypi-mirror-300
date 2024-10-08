import base64
import hashlib
import logging
import ssl
import uuid
import warnings
import webbrowser
from typing import Optional
from urllib.parse import urlencode

import jwt
import pkce
import requests

from anaconda_cli_base.console import console
from anaconda_cloud_auth import __version__
from anaconda_cloud_auth.config import AnacondaCloudConfig
from anaconda_cloud_auth.exceptions import AuthenticationError
from anaconda_cloud_auth.exceptions import InvalidTokenError
from anaconda_cloud_auth.exceptions import TokenNotFoundError
from anaconda_cloud_auth.handlers import capture_auth_code
from anaconda_cloud_auth.jwt import JWKClient
from anaconda_cloud_auth.token import TokenInfo

logger = logging.getLogger(__name__)


def _validate_access_token(
    access_token: str, algorithm_used: str, expected_hash: str
) -> None:
    """Validate the JWT token.

    We need to compute the hash of the access token and compare it with the hash that is present in the JWT.
    This is to ensure that the token is not tampered with.

    """

    # Get the standard name for the hash alg instead of the OIDC name
    hashlib_alg_name = jwt.get_algorithm_by_name(algorithm_used).hash_alg.name  # type: ignore

    hash = hashlib.new(hashlib_alg_name)
    hash.update(access_token.encode("utf-8"))
    digest = hash.digest()

    # The left half of the total hash contains the expected hash we are
    # looking for.
    # See https://openid.net/specs/openid-connect-core-1_0.html#rfc.section.3.1.3.6
    digest_truncated = digest[: (len(digest) // 2)]

    # digest_truncated is bytes, so we decode and remove the == padding in base64
    computed_hash = (
        base64.urlsafe_b64encode(digest_truncated).decode("utf-8").rstrip("=")
    )

    if computed_hash != expected_hash:
        raise jwt.InvalidSignatureError()


def _validate_token_info(
    access_token: str,
    id_token: Optional[str],
    config: Optional[AnacondaCloudConfig] = None,
) -> None:
    if id_token is None:
        # TODO: legacy IAM doesn't work w/ these validations
        return

    config = config or AnacondaCloudConfig()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    if not config.ssl_verify:
        ctx.verify_mode = ssl.CERT_NONE

    jwks_client = JWKClient(config.oidc.jwks_uri, ssl_context=ctx)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)

    try:
        # parse JWT token and verify signature
        id_info = jwt.decode(
            id_token,
            key=signing_key.key,
            algorithms=config.oidc.id_token_signing_alg_values_supported,
            audience=config.client_id,
        )
    except jwt.exceptions.PyJWTError as e:
        raise InvalidTokenError(f"Error decoding token: {e}")

    # at this point, the jwt token should be verified and good to go
    # but we still need to verify the access token
    algorithm_used = jwt.get_unverified_header(id_token)["alg"]

    if access_token is None:
        raise TokenNotFoundError("No access token found to validate")

    try:
        _validate_access_token(access_token, algorithm_used, id_info["at_hash"])
    except jwt.InvalidSignatureError:
        raise InvalidTokenError("Access token has an invalid hash.")


def make_auth_code_request_url(
    code_challenge: str, state: str, config: Optional[AnacondaCloudConfig] = None
) -> str:
    """Build the authorization code request URL."""

    if config is None:
        config = AnacondaCloudConfig()

    authorization_endpoint = config.oidc.authorization_endpoint
    client_id = config.client_id
    redirect_uri = config.redirect_uri

    params = dict(
        client_id=client_id,
        response_type="code",
        scope="openid email profile offline_access",
        state=state,
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    encoded_params = urlencode(params)
    url = f"{authorization_endpoint}?{encoded_params}"

    return url


def _send_auth_code_request(
    code_challenge: str, state: str, config: AnacondaCloudConfig
) -> None:
    """Open the authentication flow in the browser."""
    url = make_auth_code_request_url(code_challenge, state, config)
    webbrowser.open(url)


def refresh_access_token(refresh_token: str, config: AnacondaCloudConfig) -> str:
    """Refresh and save the tokens."""
    response = requests.post(
        config.oidc.token_endpoint,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": config.client_id,
        },
        verify=config.ssl_verify,
    )
    response.raise_for_status()
    response_data = response.json()

    access_token = response_data["access_token"]
    return access_token


def request_access_token(
    auth_code: str, code_verifier: str, config: AnacondaCloudConfig
) -> str:
    """Request an access token using the provided authorization code and code verifier."""
    token_endpoint = config.oidc.token_endpoint
    client_id = config.client_id
    redirect_uri = config.redirect_uri

    response = requests.post(
        token_endpoint,
        data=dict(
            grant_type="authorization_code",
            client_id=client_id,
            code=auth_code,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        ),
        verify=config.ssl_verify,
    )
    result = response.json()

    if "error" in result:
        raise AuthenticationError(
            f"Error getting JWT: {result.get('error')} - {result.get('error_description')}"
        )

    access_token = result.get("access_token")
    return access_token


def _do_auth_flow(config: Optional[AnacondaCloudConfig] = None) -> str:
    """Do the browser-based auth flow and return the short-lived access_token and id_token tuple."""
    if config is None:
        config = AnacondaCloudConfig()

    redirect_uri = config.redirect_uri
    state = str(uuid.uuid4())
    code_verifier, code_challenge = pkce.generate_pkce_pair(code_verifier_length=128)

    _send_auth_code_request(code_challenge, state, config)

    # Listen for the response
    auth_code = capture_auth_code(redirect_uri, state)
    logger.debug("Authentication successful! Getting JWT token.")

    # Do auth code exchange
    return request_access_token(auth_code, code_verifier, config)


def _login_with_username(config: Optional[AnacondaCloudConfig] = None) -> str:
    """Prompt for username and password and log in with the password grant flow."""
    warnings.warn(
        "Basic login with username/password is deprecated and will be disabled soon.",
        UserWarning,
        stacklevel=0,
    )

    if config is None:
        config = AnacondaCloudConfig()

    username = console.input("Please enter your email: ")
    password = console.input("Please enter your password: ", password=True)
    response = requests.post(
        config.oidc.token_endpoint,
        data={
            "grant_type": "password",
            "username": username,
            "password": password,
        },
        verify=config.ssl_verify,
    )
    response_data = response.json()
    response.raise_for_status()

    access_token = response_data["access_token"]
    return access_token


def _do_login(config: AnacondaCloudConfig, basic: bool) -> None:
    if basic:
        access_token = _login_with_username(config=config)
    else:
        access_token = _do_auth_flow(config=config)
    api_key = get_api_key(access_token, config.ssl_verify)
    token_info = TokenInfo(api_key=api_key, domain=config.domain)
    token_info.save()


def get_api_key(access_token: str, ssl_verify: bool = True) -> str:
    config = AnacondaCloudConfig()

    headers = {"Authorization": f"Bearer {access_token}"}

    aau_token = config.aau_token
    if aau_token is not None:
        headers["X-AAU-CLIENT"] = aau_token

    response = requests.post(
        f"https://{config.domain}/api/iam/api-keys",
        json=dict(
            scopes=["cloud:read", "cloud:write"],
            tags=[f"anaconda-cloud-auth/v{__version__}"],
        ),
        headers=headers,
        verify=ssl_verify,
    )
    if response.status_code != 201:
        console.print("Error retrieving an API key")
        raise AuthenticationError
    return response.json()["api_key"]


def _api_key_is_valid(config: AnacondaCloudConfig) -> bool:
    try:
        valid = not TokenInfo.load(config.domain).expired
    except TokenNotFoundError:
        valid = False

    return valid


def login(
    config: Optional[AnacondaCloudConfig] = None,
    basic: bool = False,
    force: bool = False,
    ssl_verify: bool = True,
) -> None:
    """Log into Anaconda.cloud and store the token information in the keyring."""
    if config is None:
        config = AnacondaCloudConfig(ssl_verify=ssl_verify)

    if force or not _api_key_is_valid(config=config):
        _do_login(config=config, basic=basic)


def logout(config: Optional[AnacondaCloudConfig] = None) -> None:
    """Log out of Anaconda.cloud."""
    if config is None:
        config = AnacondaCloudConfig()
    try:
        token_info = TokenInfo.load(domain=config.domain)
        token_info.delete()
    except TokenNotFoundError:
        pass


def is_logged_in() -> bool:
    config = AnacondaCloudConfig()
    try:
        token_info = TokenInfo.load(domain=config.domain)
    except TokenNotFoundError:
        token_info = None

    return token_info is not None
