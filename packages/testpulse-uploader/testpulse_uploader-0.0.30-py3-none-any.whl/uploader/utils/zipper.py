import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, List
from zipfile import ZipFile

from uploader.domain.domain import TestRun

logger = logging.getLogger(__name__)

excluded_dirs = (
    ".git",
    ".idea",
    ".venv",
    ".mypy_cache",
    "venv",
    "node_modules",
    "__pycache__",
)


def exclude_directory(directory: str) -> bool:
    for excluded_dir in excluded_dirs:
        if excluded_dir in directory:
            return True
    return False


def find_files(test_run: TestRun, root: Path) -> List[str]:
    test_results = []
    files_list = []
    for dirpath, _, filenames in os.walk(root):
        if exclude_directory(directory=dirpath):
            continue

        for file in filenames:
            filename = os.path.join(dirpath, file)
            rel_file = Path(filename).relative_to(root)

            files_list.append(str(rel_file))

            # Add test results
            if test_run.test_results_regex is not None:
                for tr_regex in test_run.test_results_regex:
                    if tr_regex.search(filename):
                        test_results.append(filename)

            # Add coverage results
            if test_run.coverage_results_regex is not None:
                for cr_regex in test_run.coverage_results_regex:
                    if cr_regex.search(filename):
                        test_results.append(filename)

    if not test_results:
        logger.info("We did not find any file using the REGEX passed via parameters. Please check the files are there.")
        return test_results

    logger.info(f"We found a total of {len(test_results)} test results.")

    config_file = find_config_file(test_run, root)
    if config_file:
        test_results.append(config_file)

    # Create a file with the list of files of the project
    if len(files_list) > 0:
        with open("testpulse-filelist.txt", "w") as f:
            for file in files_list:
                f.write(f"{file}\n")

            test_results.append(os.path.realpath(f.name))

    return test_results


def find_config_file(test_run: TestRun, root: Path) -> Optional[str]:
    if test_run.config_file:
        path_to_config_file = os.path.join(root, test_run.config_file)
        if os.path.exists(path_to_config_file):
            logger.info(f"Found config file in {path_to_config_file}")
            return path_to_config_file

    logger.warning("Config file did not exist, or the provided path was not correct.")
    return None


def zip_files(files_list: List[str], root: Path) -> Optional[str]:
    if not files_list:
        logger.info('Preemptive return since list of files is empty.')
        return None

    zip_file = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    with ZipFile(zip_file.name, 'w') as zip:
        for file in files_list:
            filep = Path(file)
            zip.write(filep, filep.relative_to(root))
    return zip_file.name
