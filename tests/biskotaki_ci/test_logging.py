def test_log_file_not_present_in_newly_generated_project(
    biskotaki_ci_project,
):
    """Test that the log file is not present inside the `cookiecutter.project_slug` folder"""

    # GIVEN a the log file name, the Generator produces at runtime
    # AND the expected parent directory of the log file, created at runtime
    from pathlib import Path

    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    ## Implementation Option 1
    logs_folder = Path.cwd()

    ## Implementation Option 2
    # logs_folder: Path = LOG_FILE.parent

    # WHEN we Generate a new Project, and get the Root Folder (ie repo root dir)
    runtime_generated_project: Path = biskotaki_ci_project

    # THEN we expect Logs Captured from Runtime Code execution to be written in
    # a file present inside the shell's PWD
    INTENTIONALLY_PLACED_LOG_FILE: Path = logs_folder / FILE_TARGET_LOGS
    assert INTENTIONALLY_PLACED_LOG_FILE.exists()
    assert INTENTIONALLY_PLACED_LOG_FILE.is_file()
    # assert INTENTIONALLY_PLACED_LOG_FILE.stat().st_size > 0

    # THEN we expect the unintentional behaviour to happen
    # which is another EMPTY logs file to be present also in the gen proj dir
    UNINTENTIONALLY_PLACED_LOG_FILE: Path = runtime_generated_project / FILE_TARGET_LOGS

    bug_fixed = True
    assert (bug_fixed and not UNINTENTIONALLY_PLACED_LOG_FILE.exists()) or (
        not bug_fixed
        and UNINTENTIONALLY_PLACED_LOG_FILE.exists()
        and UNINTENTIONALLY_PLACED_LOG_FILE.is_file()
        and UNINTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
    )
