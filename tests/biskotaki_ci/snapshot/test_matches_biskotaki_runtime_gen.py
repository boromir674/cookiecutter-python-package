import pytest


@pytest.mark.parametrize(
    'snapshot',
    [
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
    assert Path('cookie-py.log') in runtime_relative_paths_set, "Bug Solved?"
    assert (
        runtime_biskotaki / 'cookie-py.log'
    ).read_text() == '', "Bug Fixed, or undocumented events were logged!"
    runtime_relative_paths_set.remove(Path('cookie-py.log'))

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

    # WHEN we compare the 2 sets of relative Paths

    ## THEN, the sets should be the same
    # same dirs and files, but not necessarily same content
    assert snap_relative_paths_set == runtime_relative_paths_set

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
    runtime_changelog = runtime_biskotaki / 'CHANGELOG.rst'  # the reality

    snap_file_content = snapshot_changelog.read_text().splitlines()
    runtime_file_content = runtime_changelog.read_text().splitlines()
    assert len(snap_file_content) == len(runtime_file_content)
    assert all(
        [
            line_pair[0] == line_pair[1]
            for line_pair in [
                x
                for x in zip(snap_file_content, runtime_file_content)
                if not x[0].startswith('0.0.1')
            ]
        ]
    ), (
        f"File: CHANGELOG.rst has different content in Snapshot and Runtime\n"
        "-------------------\n"
        f"Snapshot: {snapshot_changelog}\n"
        "-------------------\n"
        f"Runtime: {runtime_changelog}\n"
        "-------------------\n"
    )

    automated_files = snap_relative_paths_set - {Path('CHANGELOG.rst')}

    for relative_path in sorted([x for x in automated_files if x.is_file()]):
        snap_file = snapshot_dir / relative_path
        runtime_file = runtime_biskotaki / relative_path

        assert snap_file.read_text() == runtime_file.read_text(), (
            f"File: {relative_path} has different content in Snapshot and Runtime\n"
            "-------------------\n"
            f"Snapshot: {snap_file}\n"
            "-------------------\n"
            f"Runtime: {runtime_file}\n"
            "-------------------\n"
        )

    # If error appears above,
    #  - either Generator has Regressed
    #  - or values of CI biskotaki changed, but snapshot was not updated
    #  - or Biskotaki yaml leverages New Features of Generator, but Snapshot was created with older/smaller feature set
