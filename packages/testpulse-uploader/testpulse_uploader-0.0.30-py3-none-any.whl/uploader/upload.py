#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path

from uploader.authentication.authentication import authenticate
from uploader.domain.test_run import create_test_run
from uploader.receiver.receiver import upload_test_results
from uploader.utils.utils import regex_pattern
from uploader.utils.zipper import find_files, zip_files

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)
sys.tracebacklimit = 0


def create_parser() -> argparse.ArgumentParser:
    """Parse known test runner arguments.

    Returns:
        argparse.Namespace: namespace of parsed argument values
    """
    parser = argparse.ArgumentParser(
                    prog='upload.py',
                    description='Upload test results for further processing',
                    epilog='testpulse-io')

    parser.add_argument(
        "-tr",
        "--test-results-regex",
        required=False,
        help="Regex pattern to find test results XML files",
        type=regex_pattern,
        action="append",
    )

    parser.add_argument(
        "-cr",
        "--coverage-results-regex",
        required=False,
        help="Regex pattern to find coverage results XML files",
        type=regex_pattern,
        action="append",
    )

    parser.add_argument(
        "-os",
        "--operating-system",
        type=str,
        help="OS where the tests run."
    )

    parser.add_argument(
        "-lv",
        "--language-version",
        type=str,
        help="Language version. For example for Python it can be 3.11, 3.12.. For Java, 17, 21, etc.."
    )

    parser.add_argument(
        "-tfv",
        "--test-framework-version",
        type=str,
        help="Version of the test framework. For example, Pytest 8.0.0"
    )

    parser.add_argument(
        "-tt",
        "--test-type",
        type=str,
        default='unit',
        help="Test type"
    )

    parser.add_argument(
        "-cf",
        "--config-file",
        type=str,
        help="Path to the config file."
    )

    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Testpulse token."
    )

    parser.add_argument(
        "--only-zip",
        action='store_true',
        help="When set to true, the tool will not upload the zip. Useful to debug the content of the zip file."
    )

    return parser


def run(args: argparse.Namespace) -> None:
    root = Path().resolve()
    test_run = create_test_run(args=args)

    # Authenticating here is not necessary, we only upload to our receiver (not to S3), so if we want to save time
    # or GH limits, we can remove the is_for and authentication. These checks are done anyway in the receiver.
    is_fork = test_run.is_fork
    if not is_fork:
        logger.info('Authenticating...')
        authenticate(test_run.organization)
        logger.info('Authenticated successfully.')
    else:
        logger.info('Identified a fork, proceeding with tokenless authentication...')

    logger.info('Finding files and zipping...')
    selected_files = find_files(test_run, root=root)
    zip_file_name = zip_files(files_list=selected_files, root=root)
    if zip_file_name is None:
        return

    logger.info(f'Saved zip file in {zip_file_name}')

    if args.only_zip:
        logger.info("Stopping here because --only-zip argument was provided.")
        return

    logger.info('Uploading to our backend server...')

    link = upload_test_results(Path(zip_file_name), test_run=test_run)

    if link is not None:
        logger.info('Upload was successful!')
        logger.info('TestPulse URL: ' + link)


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.test_results_regex is None and args.coverage_results_regex is None:
        parser.error("At least one of --test-results-regex and --coverage-results-regex required")
    run(args=args)


if __name__ == '__main__':
    main()
