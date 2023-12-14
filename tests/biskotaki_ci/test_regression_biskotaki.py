from pathlib import Path

import pytest


# the files we intend to check for, in a biskotatki geb project
# these files should help build regressoin tests, as minimum set to verify
@pytest.fixture(
    params=[
        'scripts/parse_version.py',
        'scripts/visualize-dockerfile.py',
        'scripts/visualize-ga-workflow.py',
    ]
)
def biskotaki_file_expected(request):
    return request.param


# we concern with different assertions, given the same generated project
# so we use a "fixture" to receive the same generated project, to test against


# tests on Project Generated from .github/biskotaki.yaml
def test_gen_ci_biskotaki_has_expected_files(
    biskotaki_file_expected,
    biskotaki_ci_project,
):
    ## GIVEN freshly Generated Project, with User Config '.github/biskotaki.yaml'

    ## AND a file, that we expect to be generated
    # supplied by the 'biskotaki_file_expected' fixture, passed in this test
    expected_file: str = biskotaki_file_expected
    assert isinstance(expected_file, str), f"expected_file: {expected_file} is not a string"
    expected_file_path: Path = Path(expected_file)
    # sanity that path is relative, so that we can use it to check for existence
    assert (
        not expected_file_path.is_absolute()
    ), f"expected_file_path: {expected_file_path} is not relative"

    ## WHEN we check if the generated project has the expected files
    ERROR_MSG = (
        f"File: {expected_file_path} does not exist\n"
        f"Relative File path {expected_file_path}, and gen Biskotaki Project Dir: {biskotaki_ci_project}, do not make for an existing file\n"
        f" Possible causes:\n"
        " - This could be due to the Generator failing to create the File (ie bug)\n"
        " - Could be that test is falsely expecting File in Biskotaki.\n"
        " How to fix:\n"
        " - If this is a bug, then we caught a Regressoin Error -> fix the Generator\n"
        " - If this is a false positive, then we need to update the test to not expect this file\n"
        "    For this, we should also Advertise that this file is no longer generated\n\n"
        "   Make sure we communicate this is: Docs, Readme, PR, Release Note, Sem Ver Tag, etc\n\n"
        "  It could be a 'Public API' change, hence this verbose error message\n"
    )

    assert (biskotaki_ci_project / expected_file_path).exists(), ERROR_MSG
