import os
import logging
from sys import platform
from typing import Optional

from uploader.receiver.receiver import check_is_fork
from uploader.domain.domain import TestRun
from uploader.domain.exceptions import NotInCI

logger = logging.getLogger(__name__)


class JenkinsTestRun(TestRun):
    @property
    def ci(self) -> str:
        return "JENKINS"

    @property
    def repository(self) -> str:
        if 'GIT_URL' in os.environ:
            # This env variable is something like: https://github.com/testpulse-io/testpulse-io.git
            # We need to strip the owner everything except the name of the repo
            url = os.environ['GIT_URL']
            if url.endswith(".git"):
                url = url[:-4]

            return url.split("/")[-1]
        raise NotInCI("GIT_URL")

    @property
    def operating_system(self) -> str:
        if self.args.operating_system:
            return self.args.operating_system
        if platform == "linux" or platform == "linux2":
            return "Linux"
        elif platform == "darwin":
            return "MacOS"
        elif platform == "win32":
            return "Windows"

        return platform

    @property
    def commit(self) -> str:
        if 'GIT_COMMIT' in os.environ:
            return os.environ['GIT_COMMIT']
        raise NotInCI("GIT_COMMIT")

    @property
    def organization(self) -> str:
        if 'GIT_URL' in os.environ:
            # This env variable is something like: https://github.com/testpulse-io/testpulse-io.git
            # We need to strip the owner everything except the name of the repo
            url = os.environ['GIT_URL']
            if url.endswith(".git"):
                url = url[:-4]

            return url.split("/")[-2]
        raise NotInCI("GIT_URL")

    @property
    def branch(self) -> Optional[str]:
        if 'BRANCH_NAME' in os.environ:
            return os.environ['BRANCH_NAME']
        return None

    @property
    def pull_request_number(self) -> Optional[str]:
        if 'CHANGE_ID' in os.environ:
            return os.environ['CHANGE_ID']
        return None

    @property
    def ci_run_id(self) -> Optional[str]:
        if 'JOB_NAME' in os.environ and 'BUILD_NUMBER' in os.environ:
            return f"{os.environ['JOB_NAME']}/{os.environ['BUILD_NUMBER']}"
        raise NotInCI("JOB_NAME")

    @property
    def ci_link(self) -> Optional[str]:
        if 'BUILD_URL' in os.environ:
            return os.environ['BUILD_URL']
        raise NotInCI("BUILD_URL")

    @property
    def ci_workflow(self) -> Optional[str]:
        if 'JOB_NAME' in os.environ:
            return os.environ['JOB_NAME'].replace('/' + os.environ['JOB_BASE_NAME'], '')
        raise NotInCI("JOB_NAME")

    @property
    def ci_job(self) -> Optional[str]:
        return self.ci_workflow

    @property
    def is_fork(self) -> Optional[bool]:
        pr = self.pull_request_number
        if not pr:
            return False

        return check_is_fork(f"{self.organization}/{self.repository}", pr)
