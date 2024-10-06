import os
import logging
from typing import Optional

from uploader.receiver.receiver import check_is_fork
from uploader.domain.domain import TestRun
from uploader.domain.exceptions import NotInCI

logger = logging.getLogger(__name__)


class DroneCITestRun(TestRun):
    @property
    def ci(self) -> str:
        return "DRONE"

    @property
    def repository(self) -> str:
        if 'DRONE_REPO_NAME' in os.environ:
            return os.environ['DRONE_REPO_NAME']
        raise NotInCI("DRONE_REPO_NAME")

    @property
    def operating_system(self) -> str:
        if self.args.operating_system:
            return self.args.operating_system
        if 'DRONE_STAGE_OS' in os.environ:
            return os.environ['DRONE_STAGE_OS']
        raise NotInCI("DRONE_STAGE_OS")

    @property
    def commit(self) -> str:
        if 'DRONE_COMMIT_SHA' in os.environ:
            return os.environ['DRONE_COMMIT_SHA']
        raise NotInCI("DRONE_COMMIT_SHA")

    @property
    def organization(self) -> str:
        if 'DRONE_REPO_OWNER' in os.environ:
            return os.environ['DRONE_REPO_OWNER']
        raise NotInCI("DRONE_REPO_OWNER")

    @property
    def branch(self) -> Optional[str]:
        if os.environ.get('DRONE_PULL_REQUEST', '') == '':
            # We are not in a PR, return the target branch as it's the same as the source branch
            return os.environ['DRONE_COMMIT_BRANCH']
        # We are in a PR, return the source branch
        return os.environ.get('DRONE_SOURCE_BRANCH', '')

    @property
    def pull_request_number(self) -> Optional[str]:
        if 'DRONE_PULL_REQUEST' in os.environ and os.environ['DRONE_PULL_REQUEST'] != '':
            return os.environ['DRONE_PULL_REQUEST']
        return None

    @property
    def ci_run_id(self) -> Optional[str]:
        if 'DRONE_BUILD_NUMBER' in os.environ:
            return os.environ['DRONE_BUILD_NUMBER']
        raise NotInCI("DRONE_BUILD_NUMBER")

    @property
    def ci_link(self) -> Optional[str]:
        if 'DRONE_BUILD_LINK' in os.environ:
            return os.environ['DRONE_BUILD_LINK']
        raise NotInCI("DRONE_BUILD_LINK")

    @property
    def ci_workflow(self) -> Optional[str]:
        if 'DRONE_STAGE_NAME' in os.environ:
            return os.environ['DRONE_STAGE_NAME']
        raise NotInCI("DRONE_STAGE_NAME")

    @property
    def ci_job(self) -> Optional[str]:
        return self.ci_workflow

    @property
    def is_fork(self) -> Optional[bool]:
        pr = self.pull_request_number
        if not pr:
            return False

        return check_is_fork(os.environ['DRONE_REPO'], pr)
