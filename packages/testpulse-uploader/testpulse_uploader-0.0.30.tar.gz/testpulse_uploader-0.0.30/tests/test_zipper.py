from pathlib import Path

from uploader.domain.ci.github_test_run import GitHubTestRun
from uploader.upload import create_parser
from uploader.utils.zipper import find_files


def test_find_files():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = GitHubTestRun(args=args)
    result = find_files(test_run, Path('tests/fixtures/test_results/'))
    elements = [
        'tests/fixtures/test_results/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples1/pydriller_testresults1.xml',
        'tests/fixtures/test_results/examples1/examples2/' +
        'pydriller_testresults2.xml',
    ]
    for el in elements:
        assert el in result

    found_test_list = False
    for el in result:
        if el.endswith("testpulse-filelist.txt"):
            found_test_list = True

    assert found_test_list is True
    assert len(elements) + 1 == len(result)


def test_find_files_exclude_dir():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = GitHubTestRun(args=args)
    result = find_files(test_run, Path('tests/fixtures/test_results_exclude_dirs/'))
    elements = [
        'tests/fixtures/test_results_exclude_dirs/pydriller_testresults.xml',
    ]
    for el in elements:
        assert el in result
    assert len(elements) + 1 == len(result)


def test_find_files_with_config():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml', '-cf', '.testpulse.yaml'])

    test_run = GitHubTestRun(args=args)
    result = find_files(test_run, Path('tests/fixtures/test_results/'))
    elements = [
        'tests/fixtures/test_results/.testpulse.yaml',
        'tests/fixtures/test_results/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples/pydriller_testresults.xml',
        'tests/fixtures/test_results/examples1/pydriller_testresults1.xml',
        'tests/fixtures/test_results/examples1/examples2/' +
        'pydriller_testresults2.xml',
    ]
    for el in elements:
        assert el in result
    assert len(elements) + 1 == len(result)


def test_fileslist():
    parser = create_parser()
    args = parser.parse_args(['-tr', r'.*\.xml'])

    test_run = GitHubTestRun(args=args)
    result = find_files(test_run, Path('tests/fixtures/test_results/'))

    file = None
    for res in result:
        if res.endswith("testpulse-filelist.txt"):
            file = res

    with open(file, "r") as f:
        lines = f.readlines()

    all_files = [
        "pydriller_testresults.xml",
        ".testpulse.yaml",
        "examples/pydriller_testresults.xml",
        "examples1/pydriller_testresults1.xml",
        "examples1/examples2/pydriller_testresults2.xml",
    ]

    for line in lines:
        line = line.strip()

        assert line in all_files
