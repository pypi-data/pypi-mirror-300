from logging import Logger
from urllib.parse import parse_qs, urljoin, urlparse

from connector.generated.models.handle_authorization_callback_request import (
    HandleAuthorizationCallbackRequest,
)


def parse_auth_code_and_redirect_uri(
    integration_app_id: str, logger: Logger, args: HandleAuthorizationCallbackRequest
):
    redirect_uri_with_code = args.request.redirect_uri_with_code
    logger.info(f"{integration_app_id} redirect_uri_with_code: {redirect_uri_with_code}")

    parsed_uri = urlparse(redirect_uri_with_code)
    logger.info(f"{integration_app_id} parsed_uri: {parsed_uri}")

    base_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
    logger.info(f"{integration_app_id} base_url: {base_url}")

    path = parsed_uri.path
    logger.info(f"{integration_app_id} path: {path}")

    original_redirect_uri = urljoin(base_url, path)
    logger.info(f"{integration_app_id} original_redirect_uri: {original_redirect_uri}")

    query_params = parse_qs(parsed_uri.query)
    logger.info(f"{integration_app_id} query_params: {query_params}")

    authorization_code = query_params.get("code", [None])[0]
    logger.info(f"{integration_app_id} authorization_code: {authorization_code}")

    return authorization_code, original_redirect_uri
