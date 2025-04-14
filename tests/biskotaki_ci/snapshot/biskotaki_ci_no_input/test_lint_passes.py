import sys

import pytest


@pytest.mark.slow
@pytest.mark.parametrize(
    'snapshot_name',
    [
        # LINT Biskotaki, with sphinx
        'biskotaki-no-input',
        # LINT Biskotaki Gold Standard, with mkdocs
        'biskotaki-gold-standard',
    ],
)
def test_running_lint_passes(snapshot_name, my_run_subprocess, test_root):
    """Verify Snapshot Project passes `tox -e lint` out of the box."""
    from pathlib import Path

    # LINT Biskotaki
    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / snapshot_name
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    # Programmatically run Lint, with the entrypoint we suggest, for a Dev to run
    res = my_run_subprocess(  # tox -e lint
        *[sys.executable, '-m', 'tox', '-vv', '-e', 'lint'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
        shell=False,  # prevent execution of untrusted input
    )

    # SANITY verify .tox/lint exists, when using tox 3.x
    assert (snapshot_dir / '.tox' / 'lint').exists()

    # Remove .tox/lint folder, created by tox 3.x
    import shutil

    shutil.rmtree(snapshot_dir / '.tox' / 'lint')

    # Check that Code passes Lint out of the box
    assert (
        res.exit_code == 0
    ), f"Failed to run `tox -e lint` for {snapshot_name}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"


@pytest.mark.slow
@pytest.mark.parametrize(
    'snapshot_name',
    [
        # Test Case 1: RUFF Biskotaki, with sphinx
        'biskotaki-no-input',
        # Test Case 2: RUFF Biskotaki Gold Standard, with mkdocs
        'biskotaki-gold-standard',
    ],
)
def test_running_ruff_passes(snapshot_name, my_run_subprocess, test_root):
    """Verify Snapshot Project passes `tox -e ruff` out of the box."""
    from pathlib import Path

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / snapshot_name
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    # Programmatically run Lint, with the entrypoint we suggest, for a Dev to run
    res = my_run_subprocess(  # tox -e ruff
        *[sys.executable, '-m', 'tox', '-vv', '-e', 'ruff'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
        shell=False,  # prevent execution of untrusted input
    )
    # SANITY verify .tox/ruff exists, when using tox 3.x
    assert (
        res.exit_code == 0
    ), f"Failed to run `tox -e ruff` for {snapshot_name}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"

    if (snapshot_dir / '.tox' / 'ruff').exists():
        # Remove .tox/ruff folder, created by tox 3.x
        import shutil

        shutil.rmtree(snapshot_dir / '.tox' / 'ruff')

    # VERIFIED that Generator emits python code that pass Ruff out of the box !!
