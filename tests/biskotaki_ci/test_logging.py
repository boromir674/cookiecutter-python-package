def test_log_file_not_present_in_newly_generated_project(
    biskotaki_ci_project,
):
    """Test that the log file is not present inside the `cookiecutter.project_slug` folder"""
    import sys
    running_on_windows: bool = sys.platform.startswith("win")    

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
    assert (
        # Verify the Log File is in PWD, as intented by Generator's Logging Configuration
        # should work on Linux and MacOS
        (not running_on_windows and INTENTIONALLY_PLACED_LOG_FILE.exists() and INTENTIONALLY_PLACED_LOG_FILE.is_file())
        # Verify the Log File is not in PWD, despite Generator's Logging Configuration
        # this mishhap should be expected on Windows
        or (running_on_windows and not INTENTIONALLY_PLACED_LOG_FILE.exists())
    )
    # assert INTENTIONALLY_PLACED_LOG_FILE.stat().st_size > 0

    # THEN we expect the unintentional behaviour to happen
    # which is another EMPTY logs file to be present also in the gen proj dir
    UNINTENTIONALLY_PLACED_LOG_FILE: Path = runtime_generated_project / FILE_TARGET_LOGS

    bug_fixed = True

    # exception misbehaviour fixed on Windows?
    import os
    has_developer_fixed_windows_mishap: bool = os.environ.get("BUG_LOG_DEL_WIN") != "permission_error"

    assert (
    # Expected Behaviour happens on Windows
        running_on_windows and ((
            has_developer_fixed_windows_mishap and not UNINTENTIONALLY_PLACED_LOG_FILE.exists()
        ) or (not has_developer_fixed_windows_mishap and UNINTENTIONALLY_PLACED_LOG_FILE.exists()))
    ) or (

    # Expected Behaviour happens on other Platforms
        bug_fixed and not UNINTENTIONALLY_PLACED_LOG_FILE.exists()
    ) or (

    # Document Bug behaviour
        not bug_fixed
        and UNINTENTIONALLY_PLACED_LOG_FILE.exists()
        and UNINTENTIONALLY_PLACED_LOG_FILE.is_file()
        and UNINTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
    )
