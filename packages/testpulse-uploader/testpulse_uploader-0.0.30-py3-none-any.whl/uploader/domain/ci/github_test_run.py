import os
import logging
from typing import Optional
import re

from uploader.domain.domain import TestRun
from uploader.domain.exceptions import NotInCI
from uploader.receiver.receiver import check_is_fork

logger = logging.getLogger(__name__)


class GitHubTestRun(TestRun):
    @property
    def ci(self) -> str:
        return "GITHUB"

    @property
    def repository(self) -> str:
        if 'GITHUB_REPOSITORY' in os.environ:
            # The ENV variable contains both owner and repo (like "octocat/Hello-World").
            # We need to strip the owner and only keep the repo ("Hello-World").
            owner_and_repo = os.environ['GITHUB_REPOSITORY']
            owner = f"{self.organization}/"
            if owner not in owner_and_repo:
                # VERY STRANGE scenario! Maybe the ENV variable changed?
                raise Exception(f"The ENV variable 'GITHUB_REPOSITORY' ({owner_and_repo}) "
                                f"does not contain the owner ({self.organization}).")
            return owner_and_repo.split(owner)[1]
        raise NotInCI("GITHUB_REPOSITORY")

    @property
    def operating_system(self) -> str:
        if self.args.operating_system:
            return self.args.operating_system
        if 'RUNNER_OS' in os.environ:
            return os.environ['RUNNER_OS']
        raise NotInCI("RUNNER_OS")

    @property
    def commit(self) -> str:
        if 'GITHUB_SHA' in os.environ:
            return os.environ['GITHUB_SHA']
        raise NotInCI("GITHUB_SHA")

    @property
    def organization(self) -> str:
        if 'GITHUB_REPOSITORY_OWNER' in os.environ:
            return os.environ['GITHUB_REPOSITORY_OWNER']
        raise NotInCI("GITHUB_REPOSITORY_OWNER")

    @property
    def branch(self) -> Optional[str]:
        if 'GITHUB_REF' in os.environ:
            if 'refs/heads/' in os.environ['GITHUB_REF']:
                return os.environ['GITHUB_REF'].replace('refs/heads/', '')
        return None

    @property
    def pull_request_number(self) -> Optional[str]:
        if not os.getenv("GITHUB_HEAD_REF"):
            return None

        pr_ref = os.getenv("GITHUB_REF")

        if not pr_ref:
            return None

        match = re.search(r"refs/pull/(\d+)/merge", pr_ref)

        if match is None:
            return None

        pr = match.group(1)

        return pr or None

    @property
    def ci_run_id(self) -> Optional[str]:
        if 'GITHUB_RUN_ID' in os.environ:
            return os.environ['GITHUB_RUN_ID']
        raise NotInCI("GITHUB_RUN_ID")

    @property
    def ci_link(self) -> Optional[str]:
        # Build the link to the build job. GH doesn't provide a link
        # https://github.com/ORG/REPO/actions/runs/GITHUB_RUN_ID
        server_url = os.environ['GITHUB_SERVER_URL']

        # Strip last slash, if any
        if server_url.endswith("/"):
            server_url = server_url[-1]

        repo = os.environ['GITHUB_REPOSITORY']
        github_run_id = os.environ['GITHUB_RUN_ID']

        return f"{server_url}/{repo}/actions/runs/{github_run_id}"

    @property
    def ci_workflow(self) -> Optional[str]:
        if 'GITHUB_WORKFLOW' in os.environ:
            return os.environ['GITHUB_WORKFLOW']
        raise NotInCI("GITHUB_WORKFLOW")

    @property
    def ci_job(self) -> Optional[str]:
        if 'GITHUB_JOB' in os.environ:
            return os.environ['GITHUB_JOB']
        raise NotInCI("GITHUB_JOB")

    @property
    def is_fork(self) -> Optional[bool]:
        pr = self.pull_request_number
        if not pr:
            return False

        return check_is_fork(os.environ['GITHUB_REPOSITORY'], pr)
