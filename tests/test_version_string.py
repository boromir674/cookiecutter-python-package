from pathlib import Path

import pytest


def test_version_msg_function_returns_expected_string(distro_loc: Path):
    # GIVEN the version_msg function
    from cookiecutter_python.cli import version_msg

    # WHEN the version_msg function is called
    result: str = version_msg()

    # THEN it should return the expected string
    import sys

    EXPECTED_PYTHON_VERSION: str = ".".join(map(str, sys.version_info[:3]))

    EXPECTED_PARENT_DIR_OF_COOKIECUTTER_PYTHON: Path = distro_loc.parent

    assert result == (
        f'Python Generator %(version)s from {EXPECTED_PARENT_DIR_OF_COOKIECUTTER_PYTHON} (Python {EXPECTED_PYTHON_VERSION})'
    )


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli_version_flag_returns_expected_string(
    distro_loc: Path,
    isolated_cli_runner,
):
    from cookiecutter_python import __version__
    from cookiecutter_python.cli import main

    result = isolated_cli_runner.invoke(
        main,
        args=['--version'],
        input=None,
        env=None,
        catch_exceptions=False,
    )
    assert result.exit_code == 0

    import sys

    EXPECTED_PYTHON_VERSION: str = ".".join(map(str, sys.version_info[:3]))

    EXPECTED_PARENT_DIR_OF_COOKIECUTTER_PYTHON: Path = distro_loc.parent

    assert result.stdout == (
        f'Python Generator {__version__} from {EXPECTED_PARENT_DIR_OF_COOKIECUTTER_PYTHON} (Python {EXPECTED_PYTHON_VERSION})\n'
    )
