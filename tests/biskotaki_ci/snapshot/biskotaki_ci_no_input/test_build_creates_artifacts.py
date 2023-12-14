import sys

import pytest


@pytest.mark.integration
def test_running_build_creates_source_and_wheel_distros(
    test_root,
):
    import subprocess
    from pathlib import Path

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / 'biskotaki-no-input'
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    ## Programmatically run Build, with the entrypoint we suggest, for a Dev to run
    res = subprocess.run(  # tox -e build
        [sys.executable, '-m', 'tox', '-r', '-vv', '-e', 'build'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
    )
    # CLEAN UP: Remove .tox/build folder, created by tox
    import shutil

    shutil.rmtree(snapshot_dir / '.tox' / 'build')

    # Check that Code passes Build out of the box
    assert res.returncode == 0

    # Check that Source and Wheel distros are created
    dist_dir: Path = snapshot_dir / 'dist'
    assert dist_dir.exists()
    assert dist_dir.is_dir()

    # if 'build' module is used for the Build/Package process
    # then at time of writing, it is known to place in the 'dist' target dir
    # exactly the 2 files of our Distro, and nothing else

    # if 'pip' module is used for the Build/Package process
    # then at time of writing, it is known to place in the 'dist' target dir
    # both our 2 files, but also potentially other wheels that are dependencies of our Code

    # here we ASSUME 'build' module is used for the Build/Package process
    # otherwise the below should break, which means we must update this test
    # since the 'pip' has now replaced the 'build' module for the Build/Package process

    # Check that no other distros are created
    assert len(list(dist_dir.glob('*.whl'))) == 1
    assert len(list(dist_dir.glob('*.tar.gz'))) == 1

    # Basically only 2 files should be created
    assert len(list(dist_dir.glob('*'))) == 2

    ## Programmatically run Metadata Checks on Distros, with the  entrypoint we
    # suggest, for a Dev to run

    # Check that Code passes Metadata Checks out of the box
    # run `tox -e check` and make sure we first do clean up before throwing an error
    res = subprocess.run(  # tox -e check
        [sys.executable, '-m', 'tox', '-r', '-vv', '-e', 'check'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
    )

    # CLEAN UP: Remove .tox/check folder, created by tox
    import shutil

    shutil.rmtree(snapshot_dir / '.tox' / 'check')

    # Check that Code passes Metadata Checks out of the box
    assert res.returncode == 0

    # TODO Improve by parsing the expected stdout from tox
    # we can see that Pyroma is expected to run against Source but no Wheel distros
    # Twine is expected to run aginast Sdist and Wheel distros

    """check: commands[0]> pyroma --directory /data/repos/cookiecutter-python-package/tests/data/snapshots/biskotaki-no-input
    ------------------------------
    Checking /data/repos/cookiecutter-python-package/tests/data/snapshots/biskotaki-no-input
    Getting metadata for wheel...
    Found biskotaki
    ------------------------------
    Final rating: 10/10
    Your cheese is so fresh most people think it's a cream: Mascarpone
    ------------------------------
    check: commands[1]> pyroma --file dist/biskotaki-0.0.1.tar.gz
    ------------------------------
    Checking dist/biskotaki-0.0.1.tar.gz
    Getting metadata for wheel...
    Found biskotaki
    ------------------------------
    Final rating: 10/10
    Your cheese is so fresh most people think it's a cream: Mascarpone
    ------------------------------
    check: commands[2]> python -m twine check 'dist/biskotaki-0.0.1*'
    Checking dist/biskotaki-0.0.1-py3-none-any.whl: PASSED
    Checking dist/biskotaki-0.0.1.tar.gz: PASSED
    """

    # Remove 'dist' folder, and avoid OSError: [Errno 39] Directory not empty
    for distro in dist_dir.glob('*'):
        distro.unlink()

    dist_dir.rmdir()

    assert not dist_dir.exists()
