import sys

import pytest


@pytest.mark.integration
def test_running_lint_passes(
    test_root,
):
    import subprocess
    from pathlib import Path

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / 'biskotaki-no-input'
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    # Programmatically run Lint, with the entrypoint we suggest, for a Dev to run
    res = subprocess.run(  # tox -e lint
        [sys.executable, '-m', 'tox', '-r', '-vv', '-e', 'lint'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
    )

    # Remove .tox/ folder, created by tox
    import shutil

    shutil.rmtree(snapshot_dir / '.tox')

    # Check that Code passes Lint out of the box
    assert res.returncode == 0
