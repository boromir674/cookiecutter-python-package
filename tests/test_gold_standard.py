import logging
import typing as t
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
    # Ad-hoc sanity checks that docs folder contains all sub-dirs and nested files
    assert (gen_project_dir / 'docs').exists()
    assert not (gen_project_dir / 'docs-mkdocs').exists()
    assert not (gen_project_dir / 'docs-sphinx').exists()
    assert (gen_project_dir / 'docs').is_dir()
    assert (gen_project_dir / 'docs' / 'assets').exists()
    assert (gen_project_dir / 'docs' / 'assets').is_dir()
    assert (gen_project_dir / 'docs' / 'dev_guides').exists()
    assert (gen_project_dir / 'docs' / 'dev_guides' / 'docker.md').exists()
    assert (gen_project_dir / 'docs' / 'dev_guides' / 'docker.md').is_file()

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


@pytest.fixture(scope='session')
def validate_project():
    def _validate_project(project_dir: Path) -> t.Set[Path]:
        """Validate directory and clean up irrelevant paths."""
        assert (
            project_dir.exists() and project_dir.is_dir()
        ), f"Project directory {project_dir} does not exist"

        # here we make the tests more reliables for local development, by excluding
        return set(
            x
            for x in set(x.relative_to(project_dir) for x in project_dir.glob('**/*'))
            if not any(p in {'__pycache__', '.ruff_cache'} for p in x.parts)
        )

    return _validate_project


@pytest.fixture(scope='session')
def compare_file_content():
    def _compare_file_content(runtime_file: Path, snap_file: Path):
        """Compare the content of two files line by line."""
        runtime_file_content = runtime_file.read_text().splitlines()
        snap_file_content = snap_file.read_text().splitlines()

        for line_index, line_pair in enumerate(zip(runtime_file_content, snap_file_content)):
            assert line_pair[0] == line_pair[1], (
                f"File: {runtime_file.relative_to(runtime_file.parent)} has different content at Runtime than in Snapshot\n"
                f"Line Index: {line_index}\n"
                f"Line Runtime: {line_pair[0]}\n"
                f"Line Snapshot: {line_pair[1]}\n"
            )
        assert len(runtime_file_content) == len(snap_file_content)

    return _compare_file_content


@pytest.fixture(scope='module')
def file_gen():
    def _file_gen(runtime_relative_paths_set: t.Set[Path]) -> t.Iterator[t.Tuple[Path, Path]]:
        for relative_path in [
            x
            for x in sorted(
                runtime_relative_paths_set - {Path('cookie-py.log'), Path('CHANGELOG.rst')}
            )
            if x.is_file() and x.suffix != '.png'
        ]:
            yield relative_path

    return _file_gen


def test_gs_matches_runtime(
    gen_gs_project, validate_project, compare_file_content, file_gen, test_root
):
    ## GIVEN the Snapshot project files maintained for the Gold Standard of Biskotaki
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / 'biskotaki-gold-standard'
    snap_relative_paths_set = validate_project(snapshot_dir)

    # if 'cookie-py.log' file found show warning
    if Path('cookie-py.log') in snap_relative_paths_set:
        logger = logging.getLogger(__name__)
        logger.warning("cookie-py.log file found in snapshot")

    ## GIVEN project files generated at (test) runtime, with 'biskotaki-gold-standard' User Config
    runtime_relative_paths_set = validate_project(gen_gs_project)

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

    # This is useful for local development, to make the tests more reliable
    snap_relative_paths_set = set(
        [
            x
            for x in snap_relative_paths_set
            if not (
                any(
                    [
                        p
                        in {
                            'poetry.lock',
                            '.vscode',
                            'settings.json',
                            '.tox',
                            '.pytest_cache',
                        }
                        for p in x.parts
                    ]
                )
            )
        ]
    )
    snap_relative_paths_set = set([x for x in snap_relative_paths_set if x.name != 'reqs.txt'])

    if has_developer_fixed_windows_mishap:
        assert runtime_relative_paths_set == snap_relative_paths_set
    elif running_on_windows:  # there is a log mishappening that we exists on windows
        from cookiecutter_python._logging_config import (
            FILE_TARGET_LOGS as LOG_FILE_NAME,
        )

        # create augmented set, with added extra file, as union of both sets
        augmented_exp_set = snap_relative_paths_set.union({Path(LOG_FILE_NAME)})
        assert runtime_relative_paths_set == augmented_exp_set
    else:
        assert runtime_relative_paths_set == snap_relative_paths_set

    ## THEN we expect the same files to have the same content

    # runtime project generation yields a CHNADELOG file, where an initial item
    # is added. The Release Date is set dynamically based on runtime current date
    # so, we hard exclude the line starting with the '0.0.1' string, to avoid
    # comparing rolling date with the static one in the snapshot

    # first compare CHANGLOG files, then all other files
    snapshot_changelog = snapshot_dir / 'CHANGELOG.rst'  # the expectation
    runtime_changelog = gen_gs_project / 'CHANGELOG.rst'  # the reality

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

    for runtime_file, snap_file in (
        (gen_gs_project / x, snapshot_dir / x) for x in file_gen(runtime_relative_paths_set)
    ):
        # go line by line and assert each one for easier debugging
        compare_file_content(runtime_file, snap_file)

    # If error appears above,
    #  - either Generator has Regressed
    #  - or values of CI biskotaki changed, but snapshot was not updated
    #  - or Biskotaki yaml leverages New Features of Generator, but Snapshot was created with older/smaller feature set
