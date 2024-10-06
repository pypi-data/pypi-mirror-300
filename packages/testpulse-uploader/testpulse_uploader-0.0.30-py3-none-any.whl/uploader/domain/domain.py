import logging
import os
from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Dict, Optional, Pattern, List

from uploader.domain.exceptions import NotInCI

logger = logging.getLogger(__name__)


class TestRun(ABC):
    def __init__(self, args: Namespace) -> None:
        self.args = args

    # Testpulse custom variables. Can be passed via args or via env variables.
    # REQUIRED: should throw if not found in args or env variables
    @property
    def test_results_regex(self) -> Optional[List[Pattern[str]]]:
        return self.args.test_results_regex

    @property
    def coverage_results_regex(self) -> Optional[List[Pattern[str]]]:
        return self.args.coverage_results_regex

    # NOT REQUIRED: in this case it's fine to return None
    @property
    def token(self) -> Optional[str]:
        if self.args.token:
            return self.args.token
        if 'TESTPULSE_TOKEN' in os.environ:
            return os.environ['TESTPULSE_TOKEN']
        if self.is_fork:
            return None
        raise NotInCI("TESTPULSE_TOKEN")

    @property
    def language_version(self) -> Optional[str]:
        if self.args.language_version:
            return self.args.language_version
        if 'TP_LANG_VERSION' in os.environ:
            return os.environ['TP_LANG_VERSION']
        return None

    @property
    def test_framework_version(self) -> Optional[str]:
        if self.args.test_framework_version:
            return self.args.test_framework_version
        if 'TP_TEST_FRAME_VERSION' in os.environ:
            return os.environ['TP_TEST_FRAME_VERSION']
        return None

    @property
    def config_file(self) -> Optional[str]:
        if self.args.config_file:
            return self.args.config_file
        if 'TP_CONFIG_FILE' in os.environ:
            return os.environ['TP_CONFIG_FILE']
        return None

    @property
    def test_type(self) -> Optional[str]:
        if self.args and self.args.test_type:
            return self.args.test_type
        if 'TP_TEST_TYPE' in os.environ:
            return os.environ['TP_TEST_TYPE']
        return None

    # The next ones are taken from GH default env variables.
    # They should always be != None. Otherwise it means we are not in CI.
    # https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables

    @property
    @abstractmethod
    def ci(self) -> str:
        pass

    @property
    @abstractmethod
    def repository(self) -> str:
        pass

    @property
    @abstractmethod
    def operating_system(self) -> str:
        pass

    @property
    @abstractmethod
    def commit(self) -> str:
        pass

    @property
    @abstractmethod
    def organization(self) -> str:
        pass

    @property
    @abstractmethod
    def branch(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def pull_request_number(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def ci_run_id(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def ci_link(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def ci_workflow(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def ci_job(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def is_fork(self) -> Optional[bool]:
        pass

    @property
    def test_configuration(self) -> Dict[str, str]:
        tc = {}
        if self.language_version:
            tc['languageVersion'] = self.language_version
        if self.operating_system:
            tc['operatingSystem'] = self.operating_system
        if self.test_framework_version:
            tc['testFrameworkVersion'] = self.test_framework_version

        return tc


class TokenVerification:
    @property
    def token(self) -> str:
        if 'TESTPULSE_TOKEN' in os.environ:
            return os.environ['TESTPULSE_TOKEN']
        raise NotInCI("TESTPULSE_TOKEN")
