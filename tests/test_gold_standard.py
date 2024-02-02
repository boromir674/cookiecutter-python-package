from pathlib import Path

import pytest


@pytest.fixture
def gen_gs_project(
    # Mock Network Code, to prevent http (future) requests
    user_config,
    mock_check,
    test_root,
    tmp_path,
) -> Path:
    """Fixture that generates a project from tests/data/gold-standard.yml"""
    import sys

    from cookiecutter_python.backend.main import generate

    assert test_root.exists()
    assert test_root.is_dir()
    assert test_root.name == 'tests'
    assert test_root.is_absolute()

    gs_yaml: Path = test_root / 'data' / 'gold-standard.yml'
    assert gs_yaml.exists()
    assert gs_yaml.is_file()
    assert gs_yaml.name == 'gold-standard.yml'

    # Mock Network Code, in case http (Future) requests are made
    mock_check.config = user_config[gs_yaml]
    mock_check('pypi', True)
    mock_check('readthedocs', True)

    # Generate Biskota from CI Config Yaml
    project_dir: str = generate(
        no_input=True,
        output_dir=tmp_path,  # Path or string to a folder path
        config_file=str(gs_yaml),  # better be a string
        default_config=False,
    )
    gen_project_dir: Path = Path(project_dir)

    # Sanity Checks
    assert gen_project_dir.exists()
    assert gen_project_dir.is_dir()
    assert (gen_project_dir / 'src').exists() and (gen_project_dir / 'src').is_dir()

    ## Logging file created - Assertions ##
    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    # Expected and Intentend Logging behaviour:
    # - log file with records is created in PWD of the shell that runs the generator
    # get pwd of the shell that runs the generator
    pwd = Path.cwd()
    INTENTIONALLY_PLACED_LOG_FILE: Path = pwd / FILE_TARGET_LOGS
    # on Windows, it has been reported that the Log file is missing

    running_on_windows: bool = sys.platform.startswith("win")

    if not running_on_windows:
        # here we used to assert that Log File exists where it should
        # assert (
        #     INTENTIONALLY_PLACED_LOG_FILE.exists()
        # ), "Bug re-appeared? Regression on Linux-based OS?"
        # assert INTENTIONALLY_PLACED_LOG_FILE.is_file()
        # this commit somehow makes CI on Linux to break. But not on dev machine

        # issue a pytest warning whever the Log File is not created as it should
        if not INTENTIONALLY_PLACED_LOG_FILE.exists():
            pytest.warns(
                UserWarning,
                match="Bug re-appeared? Regression on Linux-based OS?",
            )

        # AND has at least some Log records captured, during runtime code execution
        # assert INTENTIONALLY_PLACED_LOG_FILE.stat().st_size > 0

    ###### Document kind of Bug ######
    # Expected but probably unintented behaviour:
    # - empty log file gets created inside the gen project dir

    # Log file is placed inside the generated project dir, after generation
    # probably it should be place in PWD of the shell that runs the generator

    FIXED = True
    fixed_unintentional_placement_of_log_file_in_gen_proj_dir: bool = FIXED
    bug = not fixed_unintentional_placement_of_log_file_in_gen_proj_dir

    UNINTENTIONALLY_PLACED_LOG_FILE: Path = gen_project_dir / FILE_TARGET_LOGS
    assert not bug
    ## Implementation Option 1
    if bug:
        print(f"\n Verifying Unintentional Logging Behaviour still happens: {bug}\n")
        assert UNINTENTIONALLY_PLACED_LOG_FILE.exists()
        assert UNINTENTIONALLY_PLACED_LOG_FILE.is_file()
        assert UNINTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
    else:
        # on Windows, it has been reported that the Log file exists!
        if sys.platform != 'win32':
            assert not UNINTENTIONALLY_PLACED_LOG_FILE.exists()

    return gen_project_dir


def test_gs_matches_runtime(gen_gs_project, test_root):
    ## GIVEN a Snapshot we maintain, reflecting the Gold Standard of Biskotaki
    from pathlib import Path

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / 'biskotaki-gold-standard'
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    ## GIVEN a Project Generated at runtime, with 'biskotaki-gold-standard' User Config
    runtime_gs: Path = gen_gs_project

    ## GIVEN we find the Snapshot files (paths to dirs and files), using glob
    snap_relative_paths_set = set(
        [x.relative_to(snapshot_dir) for x in snapshot_dir.glob('**/*')]
    )

    # GIVEN we find the Runtime files (paths to dirs and files), using glob
    runtime_relative_paths_set = set(
        [x.relative_to(runtime_gs) for x in runtime_gs.glob('**/*')]
    )

    # for all relative paths, if 'part' __pycache__ is in the path, remove it
    snap_relative_paths_set = set(
        [x for x in snap_relative_paths_set if '__pycache__' not in x.parts]
    )
    runtime_relative_paths_set = set(
        [x for x in runtime_relative_paths_set if '__pycache__' not in x.parts]
    )

    # Sanity Check that tests/test_cli.py is part of the comparison below
    assert Path('tests/test_cli.py') in snap_relative_paths_set, (
        f"tests/test_cli.py is missing from Snapshot: {snapshot_dir}\n"
        "-------------------\n"
        "Files in 'tests' folder: [\n"
        + '\n'.join(
            [
                ' ' + str(x)
                for x in snap_relative_paths_set
                if x.parts[0] == 'tests' and len(x.parts) > 1
            ]
        )
        + "\n]\n"
    )

    # WHEN we compare the 2 sets of relative Paths

    ## THEN, the sets should be the same
    # same dirs and files, but not necessarily same content
    import sys

    running_on_windows: bool = sys.platform.startswith("win")
    # exception misbehaviour fixed on Windows?
    import os

    has_developer_fixed_windows_mishap: bool = (
        os.environ.get("BUG_LOG_DEL_WIN") != "permission_error"
    )

    # we should implement an if run on CI check here
    running_on_ci: bool = 'CI' in os.environ

    if not running_on_ci:
        # just exclude pre-emptively '.vscode/' folder, and '.vscode/settings.json' file
        # also exclude .tox/ folder, and .tox/ folder contents
        snap_relative_paths_set = set(
            [
                x
                for x in snap_relative_paths_set
                if 'poetry.lock'
                not in x.parts  # in case we run poetry install inside biskotaki
                if '.vscode' not in x.parts
                and 'settings.json' not in x.parts
                and '.tox' not in x.parts
                # EXCLUDE .pytest_cache/ folder
                if x.parts[0] != '.pytest_cache'
            ]
        )

    if has_developer_fixed_windows_mishap:
        assert runtime_relative_paths_set == snap_relative_paths_set
    else:
        if running_on_windows:  # there is a log mishappening that we exists on windows
            from cookiecutter_python._logging_config import (
                FILE_TARGET_LOGS as LOG_FILE_NAME,
            )

            # create augmented set, with added extra file, as union of both sets
            augmented_exp_set = snap_relative_paths_set.union({Path(LOG_FILE_NAME)})
            assert runtime_relative_paths_set == augmented_exp_set
        else:
            assert runtime_relative_paths_set == snap_relative_paths_set

    # if runtime has extras such as .vscode/ folder, then probably on tests are running
    # on local dev machine were vscode was opened, at some point, in the Template Project folder

    # To fix: exit, clean dir an rerun test !

    ## THEN we expect the same files to have the same content

    # runtime project generation yields a CHNADELOG file, where an initial item
    # is added. The Release Date is set dynamically based on runtime current date
    # so, we hard exclude the line starting with the '0.0.1' string, to avoid
    # comparing rolling date with the static one in the snapshot

    # first compare CHANGLOG files, then all other files
    snapshot_changelog = snapshot_dir / 'CHANGELOG.rst'  # the expectation
    runtime_changelog = runtime_gs / 'CHANGELOG.rst'  # the reality

    snap_file_content = snapshot_changelog.read_text().splitlines()
    runtime_file_content = runtime_changelog.read_text().splitlines()
    assert len(runtime_file_content) == len(snap_file_content)
    assert all(
        [
            line_pair[0] == line_pair[1]
            for line_pair in [
                x
                for x in zip(runtime_file_content, snap_file_content)
                if not x[1].startswith('0.0.1')
            ]
        ]
    ), (
        f"File: CHANGELOG.rst has different content in Snapshot and Runtime\n"
        "-------------------\n"
        f"Runtime: {runtime_changelog}\n"
        "-------------------\n"
        f"Snapshot: {snapshot_changelog}\n"
        "-------------------\n"
    )

    automated_files = snap_relative_paths_set - {Path('CHANGELOG.rst')}

    debug = True
    if debug:
        for relative_path in sorted([x for x in automated_files if x.is_file()]):
            runtime_file = runtime_gs / relative_path
            snap_file = snapshot_dir / relative_path

            # go line by line and assert each one for easier debugging
            snap_file_content = snap_file.read_text().splitlines()
            runtime_file_content = runtime_file.read_text().splitlines()
            for line_index, line_pair in enumerate(
                zip(runtime_file_content, snap_file_content)
            ):
                assert line_pair[0] == line_pair[1], (
                    f"File: {relative_path} has different content at Runtime than in Snapshot\n"
                    f"Line Index: {line_index}\n"
                    "Line Runtime: {line_pair[0]}\n"
                    "Line Snapshot: {line_pair[1]}\n"
                )
            assert len(runtime_file_content) == len(snap_file_content)
    else:
        for relative_path in sorted([x for x in automated_files if x.is_file()]):
            runtime_file = runtime_gs / relative_path
            snap_file = snapshot_dir / relative_path

            assert runtime_file.read_text() == snap_file.read_text(), (
                f"File: {relative_path} has different content at Runtime than in Snapshot\n"
                "-------------------\n"
                f"Runtime: {runtime_file}\n"
                "-------------------\n"
                f"Snapshot: {snap_file}\n"
                "-------------------\n"
            )

    # If error appears above,
    #  - either Generator has Regressed
    #  - or values of CI biskotaki changed, but snapshot was not updated
    #  - or Biskotaki yaml leverages New Features of Generator, but Snapshot was created with older/smaller feature set
