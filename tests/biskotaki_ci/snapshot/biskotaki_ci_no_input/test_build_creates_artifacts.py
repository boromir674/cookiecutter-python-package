import sys

import pytest


@pytest.mark.slow
def test_running_build_creates_source_and_wheel_distros(
    test_root,
    my_run_subprocess,
):
    """Build wheel of biskotaki-no-input Snapshot Project and run tox -e check."""
    from pathlib import Path

    # Load Snapshot
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / 'biskotaki-no-input'
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    ## Programmatically run Build, with the entrypoint we suggest, for a Dev to run
    res = my_run_subprocess(  # tox -e build
        *[sys.executable, '-m', 'tox', '-r', '-vv', '-e', 'build'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
        shell=False,  # prevent execution of untrusted input
    )
    # shell = False causes know CWE with LOW Severity
    # >> Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
    #    Severity: Low   Confidence: High
    #    CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
    #    More Info: https://bandit.readthedocs.io/en/1.7.7/plugins/b603_subprocess_without_shell_equals_true.html

    # but if we mitigate it by setting shell=True, then we get another CWE with HIGH Severity!
    # >> Issue: [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True identified, security issue.
    #    Severity: High   Confidence: High
    #    CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
    #    More Info: https://bandit.readthedocs.io/en/1.7.7/plugins/b602_subprocess_popen_with_shell_equals_true.html

    # CLEAN UP: Remove .tox/build folder, created by tox
    import shutil

    try:
        shutil.rmtree(snapshot_dir / '.tox' / 'build')
    except FileNotFoundError:
        import logging

        logger = logging.getLogger(__name__)
        logger.warning("No .tox/build folder found to clean up")

    # Check that Code passes Build out of the box
    assert (
        res.exit_code == 0
    ), f"Build failed with return code {res.exit_code}\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}\n"

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
    res = my_run_subprocess(  # tox -e check
        *[sys.executable, '-m', 'tox', '-r', '-vv', '-e', 'check'],
        cwd=snapshot_dir,
        check=False,  # prevent raising exception, so we can do clean up
        shell=False,  # prevent execution of untrusted input
        env={
            # required by Check environment
            'PKG_VERSION': '0.0.1',
            # required due to programmatic execution, in this case
            'PATH': str(Path(sys.executable).parent),
        },
    )

    # CLEAN UP: Remove .tox/check folder, created by tox
    import shutil

    shutil.rmtree(snapshot_dir / '.tox' / 'check')

    # Check that Code passes Metadata Checks out of the box
    assert res.exit_code == 0

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
