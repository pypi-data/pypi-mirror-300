import logging

import requests

from uploader.domain.domain import TokenVerification
from uploader.domain.exceptions import HTTPRequestFailed
from uploader.utils.urls import ENDPOINT_TOKENS_CHECK, TESTPULSE_API, TESTPULSE_API_STAGING
from uploader.utils.utils import is_local_dev, is_staging

logger = logging.getLogger(__name__)


def authenticate(organization_name) -> None:
    token_verifier = TokenVerification()

    payload = {
        'token': token_verifier.token,
        'organizationName': organization_name
    }

    url = get_authenticate_url()
    req = requests.get(url=url, params=payload)

    if req.status_code != 200:
        logger.error('The token validation request failed.')
        raise HTTPRequestFailed("The token validation request failed. Make sure the token and "
                                "the organizations are valid.")


def get_authenticate_url():
    url = TESTPULSE_API
    if is_local_dev():
        url = "http://127.0.0.1:8080"
    elif is_staging():
        url = TESTPULSE_API_STAGING
    url = url + ENDPOINT_TOKENS_CHECK

    return url
