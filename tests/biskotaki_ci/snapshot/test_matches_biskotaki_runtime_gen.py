import pytest


@pytest.mark.parametrize(
    'snapshot',
    [  # add Biskotaki snapshots here, for automated testing
        'biskotaki-no-input',
        'biskotaki-interactive',
    ],
)
def test_snapshot_matches_runtime(snapshot, biskotaki_ci_project, test_root):
    ## GIVEN a Snapshot we maintain, reflecting the Gold Standard of Biskotaki
    from pathlib import Path

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / snapshot
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    ## GIVEN a Project Generated at runtime, with '.github/biskotaki.yaml' User Config
    runtime_biskotaki: Path = biskotaki_ci_project

    ## GIVEN we find the Snapshot files (paths to dirs and files), using glob
    snap_relative_paths_set = set(
        [x.relative_to(snapshot_dir) for x in snapshot_dir.glob('**/*')]
    )

    # GIVEN we find the Runtime files (paths to dirs and files), using glob
    runtime_relative_paths_set = set(
        [x.relative_to(runtime_biskotaki) for x in runtime_biskotaki.glob('**/*')]
    )

    # GIVEN that wheel files might appear in runtime, but not in snapshot
    # if runtiume has cookie-py.log , this expected based on the current behaviour of logger
    # we want to change that behaviour, so that cookie-py.log is not created there
    # assert Path('cookie-py.log') in runtime_relative_paths_set, "Bug Solved?"
    # assert (
    #     runtime_biskotaki / 'cookie-py.log'
    # ).read_text() == '', "Bug Fixed, or undocumented events were logged!"
    # runtime_relative_paths_set.remove(Path('cookie-py.log'))

    # assert Path('cookie-py.log') in snap_relative_paths_set, f"Bug Solved?"
    # assert (snapshot_dir / 'cookie-py.log').read_text() == '', f"Bug Fixed, or undocumented events were logged!"
    # snap_relative_paths_set.remove(Path('cookie-py.log'))

    # current CI runs tox -e dev, sdist, and wheel meaning it is certain __pycache__ will be created
    # remove all __pycache__ folders and everything nested under them
    # this is a tiny bit of a hack, but it is the simplest way to fix the problem

    # for all relative paths, if 'part' __pycache__ is in the path, remove it
    snap_relative_paths_set = set(
        [x for x in snap_relative_paths_set if '__pycache__' not in x.parts]
    )
    runtime_relative_paths_set = set(
        [x for x in runtime_relative_paths_set if '__pycache__' not in x.parts]
    )

    # EXCLUDE from test .pytest_cache/ folders too
    snap_relative_paths_set = set(
        [x for x in snap_relative_paths_set if '.pytest_cache' not in x.parts]
    )
    runtime_relative_paths_set = set(
        [x for x in runtime_relative_paths_set if '.pytest_cache' not in x.parts]
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

    # if running on CI
    RUNNING_ON_CI: bool = 'CI' in os.environ

    if not RUNNING_ON_CI:
        # just exclude pre-emptively '.vscode/' folder, and '.vscode/settings.json' file
        # also exclude .tox/ folder, and .tox/ folder contents
        snap_relative_paths_set = set(
            [
                x
                for x in snap_relative_paths_set
                if 'poetry.lock' not in x.parts
                if '.vscode' not in x.parts
                and 'settings.json' not in x.parts
                and '.tox' not in x.parts
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
    runtime_changelog = runtime_biskotaki / 'CHANGELOG.rst'  # the reality
    snapshot_changelog = snapshot_dir / 'CHANGELOG.rst'  # the expectation

    runtime_file_content = runtime_changelog.read_text().splitlines()
    snap_file_content = snapshot_changelog.read_text().splitlines()
    assert len(runtime_file_content) == len(snap_file_content)

    line_pairs_generator = iter(
        [
            line_pair
            for line_pair in [
                x
                for x in zip(runtime_file_content, snap_file_content)
                if not x[0].startswith('0.0.1')
            ]
        ]
    )

    if RUNNING_ON_CI:  # quickly do sanity check
        assert all([line_pair[0] == line_pair[1] for line_pair in line_pairs_generator]), (
            f"File: CHANGELOG.rst has different content at Runtime vs Snapshot\n"
            "-------------------\n"
            f"Runtime: {runtime_changelog}\n"
            "-------------------\n"
            f"Snapshot: {snapshot_changelog}\n"
            "-------------------\n"
        )
    else:  # sanity check indicating the exact failling line in case of error
        for line_pair in line_pairs_generator:
            assert line_pair[0] == line_pair[1], (
                f"File: CHANGELOG.rst has different content at Runtime vs Snapshot\n"
                "-------------------\n"
                f"Runtime: {runtime_changelog}\n"
                "-------------------\n"
                f"Snapshot: {snapshot_changelog}\n"
                "-------------------\n"
                f"Line: {line_pair[0]}\n"
                "-------------------\n"
            )

    # Remove CHANGELOG.rst from Automatic Comparison
    automated_files = snap_relative_paths_set - {Path('CHANGELOG.rst')}

    # THEN Compare docs/conf.py to disregard Calendar Year of Snapshot Creation vs Runtime
    runtime_conf = runtime_biskotaki / 'docs' / 'conf.py'  # the reality
    snapshot_conf = snapshot_dir / 'docs' / 'conf.py'  # the expectation

    runtime_file_content = runtime_conf.read_text().splitlines()
    snap_file_content = snapshot_conf.read_text().splitlines()

    assert len(runtime_file_content) == len(snap_file_content)
    line_pairs_generator = iter(
        line_pair
        for line_pair in [
            x
            for x in zip(runtime_file_content, snap_file_content)
            if not (x[1].startswith('release =') or 'year=' in x[1])
        ]
    )
    if RUNNING_ON_CI:  # quickly do sanity check
        assert all([line_pair[0] == line_pair[1] for line_pair in line_pairs_generator]), (
            f"File: docs/conf.py has different content at Runtime vs Snapshot\n"
            "-------------------\n"
            f"Runtime: {runtime_conf}\n"
            "-------------------\n"
            f"Snapshot: {snapshot_conf}\n"
            "-------------------\n"
        )
    else:  # sanity check indicating the exact failling line in case of error
        for line_pair in line_pairs_generator:
            assert line_pair[0] == line_pair[1], (
                f"File: docs/conf.py has different content at Runtime vs Snapshot\n"
                "-------------------\n"
                f"Runtime: {runtime_conf}\n"
                "-------------------\n"
                f"Snapshot: {snapshot_conf}\n"
                "-------------------\n"
                f"Line: {line_pair[0]}\n"
                "-------------------\n"
            )

    # Remove docs/conf.py from Automatic Comparison
    automated_files = automated_files - {Path('docs/conf.py')}

    ## AUTOMATIC Snapshot COMPARISON ##

    for relative_path in sorted([x for x in automated_files if x.is_file()]):
        runtime_file = runtime_biskotaki / relative_path
        snap_file = snapshot_dir / relative_path

        assert runtime_file.read_text() == snap_file.read_text(), (
            f"File: {relative_path} has different content at Runtime vs Snapshot\n"
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
