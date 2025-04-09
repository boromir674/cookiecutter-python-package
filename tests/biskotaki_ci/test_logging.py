from pathlib import Path

import pytest


@pytest.fixture
def biskotaki_ci_like_gen_proj(tmp_path):
    from cookiecutter_python.backend.main import generate

    # GIVEN any existing valid config file to use in generation
    config_file: Path = tmp_path / 'any_valid_config_file.yml'

    config_file.write_text(
        """
default_context:
    project_name: Anything Project
    full_name: GG ELA
    author: GG ELA
    email: GG.ELA@email.com
    github_username: ggela1234567
    project_short_description: Project generated using https://github.com/boromir674/cookiecutter-python-package
    initialize_git_repo: 'no'
    interpreters: {"supported-interpreters": ["3.8", "3.9", "3.10", "3.11", "3.12"]}
    docs_builder: "mkdocs"
    rtd_python_version: "3.11"
    cicd: 'stable'
"""
    )

    ######## GENERATE Biskotaki from CI Config Yaml ########
    project_dir: str = generate(
        no_input=True,
        offline=True,
        output_dir=tmp_path / 'gen',  # Path or string to a folder path
        config_file=str(config_file),  # better be a string
        default_config=False,
    )
    return Path(project_dir)


def test_log_file_not_present_in_newly_generated_project(
    biskotaki_ci_like_gen_proj,
):
    """Test that the log file is not present inside the `cookiecutter.project_slug` folder"""
    import sys

    running_on_windows: bool = sys.platform.startswith("win")

    # exception misbehaviour fixed on Windows?
    import os

    has_developer_mitigated_windows_glitch: bool = (
        os.environ.get("BUG_LOG_DEL_WIN") != "permission_error"
    )

    # GIVEN a the log file name, the Generator produces at runtime
    # AND the expected parent directory of the log file, created at runtime
    from pathlib import Path

    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    ## Implementation Option 1
    logs_folder = Path.cwd()

    ## Implementation Option 2
    # logs_folder: Path = LOG_FILE.parent

    # WHEN we Generate a new Project, and get the Root Folder (ie repo root dir)
    runtime_generated_project: Path = biskotaki_ci_like_gen_proj

    # THEN we expect Logs Captured from Runtime Code execution to be written in
    # a file present inside the shell's PWD
    INTENTIONALLY_PLACED_LOG_FILE: Path = logs_folder / FILE_TARGET_LOGS

    if not running_on_windows:
        assert not INTENTIONALLY_PLACED_LOG_FILE.exists() or (
            INTENTIONALLY_PLACED_LOG_FILE.is_file()
            and INTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
        )
    else:  # handle windows as special case to account for Log mishap
        # if running this Unit Test along with the 2 Snapshot tests, on Windows,
        # then it is expected that 'Intentional Log' file is MISSING -> mishap
        # assert not INTENTIONALLY_PLACED_LOG_FILE.exists()
        # if running ALL Unit Tests,, on Windows,
        # then it is expected that 'Intentional Log' file is Present!
        # assert INTENTIONALLY_PLACED_LOG_FILE.exists()

        # at the end it is observed that the above has a random behaviour
        # it can or cannot exist on windows, so we skip assertion
        pass

    # assert INTENTIONALLY_PLACED_LOG_FILE.stat().st_size > 0

    # THEN we expect the unintentional behaviour to happen
    # which is another EMPTY logs file to be present also in the gen proj dir
    UNINTENTIONALLY_PLACED_LOG_FILE: Path = runtime_generated_project / FILE_TARGET_LOGS

    bug_fixed = True

    # exception misbehaviour fixed on Windows?
    import os

    has_developer_mitigated_windows_glitch = (
        os.environ.get("BUG_LOG_DEL_WIN") != "permission_error"
    )

    assert (
        (
            # Expected Behaviour happens on Windows
            running_on_windows
            and (
                (
                    has_developer_mitigated_windows_glitch
                    and not UNINTENTIONALLY_PLACED_LOG_FILE.exists()
                )
                or (
                    not has_developer_mitigated_windows_glitch
                    and UNINTENTIONALLY_PLACED_LOG_FILE.exists()
                )
            )
        )
        or (
            # Expected Behaviour happens on other Platforms
            bug_fixed
            and not UNINTENTIONALLY_PLACED_LOG_FILE.exists()
        )
        or (
            # Document Bug behaviour
            not bug_fixed
            and UNINTENTIONALLY_PLACED_LOG_FILE.exists()
            and UNINTENTIONALLY_PLACED_LOG_FILE.is_file()
            and UNINTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
        )
    )
