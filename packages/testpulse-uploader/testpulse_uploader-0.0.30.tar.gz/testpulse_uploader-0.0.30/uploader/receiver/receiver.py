import json
import logging
from pathlib import Path
from typing import Optional

import requests

from uploader.domain.domain import TestRun
from uploader.utils.urls import (
    TESTPULSE_RECEIVER,
    TESTPULSE_RECEIVER_STAGING,
    ENDPOINT_UPLOAD_RESULTS,
    ENDPOINT_IS_FORK
)
from uploader.utils.utils import is_local_dev, is_staging

logger = logging.getLogger(__name__)

LOCAL_URL = 'http://127.0.0.1:8000'


def upload_test_results(zip: Path, test_run: TestRun) -> Optional[str]:
    files = {'file': open(zip, 'rb')}

    data = {
        "commit_id": test_run.commit,
        "repository": test_run.repository,
        "organization": test_run.organization,
        "ci": test_run.ci,
    }

    if test_run.ci_run_id:
        data["ci_run_id"] = test_run.ci_run_id

    if test_run.ci_link:
        data["ci_link"] = test_run.ci_link

    if test_run.ci_workflow:
        data["ci_workflow"] = test_run.ci_workflow

    if test_run.ci_job:
        data["ci_job"] = test_run.ci_job

    if test_run.test_configuration:
        data['test_configuration'] = json.dumps(test_run.test_configuration)

    if test_run.test_type:
        data['test_type'] = test_run.test_type

    if test_run.pull_request_number:
        data['pull_request_number'] = str(test_run.pull_request_number)

    if test_run.branch:
        data['branch'] = test_run.branch

    headers = {
        "Authorization": f"Bearer {test_run.token}",
    }

    url = get_receiver_url()
    url = url + ENDPOINT_UPLOAD_RESULTS

    logging.debug(f'Making request to {url}')

    req = requests.post(url=url,
                        files=files,
                        data=data,
                        headers=headers)
    if req.status_code != 200:
        logging.error(f'Something went wrong: {req.text}')
        return None

    response = req.json()

    if 'link' not in response:
        logging.error(f'Did not receive a valid response: {response}')
        return None

    return response['link']


def check_is_fork(slug: str, pr_number: str) -> bool:
    params = {
        "slug": slug,
        "pr_number": pr_number
    }

    url = get_receiver_url()
    url = url + ENDPOINT_IS_FORK

    logging.debug(f'Making request to {url}')

    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        result = response.json()

        return bool(result['is_fork'])

    return False


def get_receiver_url():
    url = TESTPULSE_RECEIVER
    if is_local_dev():
        url = 'http://127.0.0.1:8000'
    elif is_staging():
        url = TESTPULSE_RECEIVER_STAGING

    return url
