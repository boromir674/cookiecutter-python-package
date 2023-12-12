import pytest


@pytest.mark.integration
def test_running_lint_passes(
    test_root,
):
    from pathlib import Path
    import subprocess

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / 'biskotaki-no-input'
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    # Programmatically run Lint, with the entrypoint we suggest, for a Dev to run
    res = subprocess.run(  # tox -e lint
        ['tox', '-e', 'lint'],
        cwd=snapshot_dir,
        check=True,
    )

    # Check that Code passes Lint out of the box
    assert res.returncode == 0
