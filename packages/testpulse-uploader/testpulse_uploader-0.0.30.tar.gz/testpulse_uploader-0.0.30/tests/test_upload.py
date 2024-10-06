import os
import responses

from pathlib import Path
from unittest import mock

from uploader.domain.ci.github_test_run import GitHubTestRun
from uploader.upload import create_parser
from uploader.receiver.receiver import upload_test_results
from uploader.utils.urls import ENDPOINT_UPLOAD_RESULTS, TESTPULSE_RECEIVER

env_variables_mocked = {
    "GITHUB_REPOSITORY": "testpulse/myrepo",
    "GITHUB_SHA": "0289dbc9db2214d7b3e2a115987c3067b4400f25",
    "GITHUB_REF": "refs/remotes/origin/main",
    "TESTPULSE_TOKEN": "MYVERYLONGANDIMPOSSIBLETOGUESSTOKEN",
    "GITHUB_ACTIONS": "True",
    "GITHUB_RUN_ID": "8159919366",
    "GITHUB_REPOSITORY_OWNER": "testpulse",
    "RUNNER_OS": "Windows",
    "GITHUB_WORKFLOW": "My workflow",
    "GITHUB_JOB": "job1",
    "GITHUB_SERVER_URL": "github.com",
    "GITHUB_EVENT_NAME": "pull_request",
    "GITHUB_ACTOR": "ishepard",
}

url = TESTPULSE_RECEIVER + ENDPOINT_UPLOAD_RESULTS


@responses.activate
@mock.patch.dict(os.environ, env_variables_mocked)
def test_simple_false():
    # Register via 'Response' object
    rsp1 = responses.Response(
        method="POST",
        url=url,
        status=404
    )
    responses.add(rsp1)

    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = GitHubTestRun(args)
    resp2 = upload_test_results(zip=Path('tests/fixtures/test_results.zip'),
                                test_run=test_run)

    assert resp2 is None


@responses.activate
@mock.patch.dict(os.environ, env_variables_mocked)
def test_simple_true():
    # Register via 'Response' object
    rsp1 = responses.Response(
        method="POST",
        url=url,
        status=200,
        json={"link": "mylink"}
    )
    responses.add(rsp1)

    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = GitHubTestRun(args)
    resp2 = upload_test_results(zip=Path('tests/fixtures/test_results.zip'),
                                test_run=test_run)

    assert resp2 == "mylink"
