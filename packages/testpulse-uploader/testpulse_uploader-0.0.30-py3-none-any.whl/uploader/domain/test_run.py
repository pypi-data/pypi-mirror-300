import logging
import os
from argparse import Namespace

from uploader.domain.domain import TestRun
from uploader.domain.ci.drone_ci_test_run import DroneCITestRun
from uploader.domain.ci.github_test_run import GitHubTestRun
from uploader.domain.ci.jenkins_test_run import JenkinsTestRun

logger = logging.getLogger(__name__)


def create_test_run(args: Namespace) -> TestRun:
    if 'GITHUB_JOB' in os.environ:
        logger.info("GitHub detected...")
        return GitHubTestRun(args=args)
    if 'JENKINS_URL' in os.environ:
        logger.info("Jenkins detected...")
        return JenkinsTestRun(args=args)
    if 'DRONE' in os.environ:
        logger.info("Drone detected...")
        return DroneCITestRun(args=args)

    raise Exception("We did not detect a supported CI. Please send us a message and "
                    "we will reply ASAP: contact@testpulse.io")
