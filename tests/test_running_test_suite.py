import os
import sys

import pytest


@pytest.fixture
def environment():
    def get_environment_variables(project_dir: str):
        environment_variables = {
            'PYTHONPATH': f'{str(os.path.join(project_dir, "src"))}',
        }
        if sys.platform in ('linux', 'cygwin'):  # ie we are on a Linux-like OS
            return dict(
                environment_variables,
                **{'LC_ALL': 'C.UTF-8', 'LANG': 'C.UTF-8'},
            )
        if sys.platform == 'darwin':  # ie we are on a Mac OS
            return dict(
                environment_variables,
                **{'LC_ALL': 'en_GB.UTF-8', 'LANG': 'en_GB.UTF-8'},
            )
        if sys.platform == 'win32':  # ie we are on a Windows OS
            return dict(
                environment_variables,
                **{
                    'LC_ALL': 'C.UTF-8',
                    'LANG': 'C.UTF-8',
                    'PYTHONHASHSEED': '2577074909',
                },
            )
        raise RuntimeError(f'Unexpected System Found: {sys.platform}')

    return get_environment_variables


@pytest.mark.skipif(sys.platform == 'win32', reason="not working out-of-the-box for Windows")
def test_running_pytest(environment, run_subprocess, project_dir):
    result = run_subprocess(
        sys.executable,
        '-m',
        'pytest',
        '-s',
        '-ra',
        '-vv',
        os.path.join(project_dir, 'tests'),
        check=False,
        env=environment(project_dir),
    )
    assert ' failed' not in result.stdout
    assert result.stderr == ''
    assert result.exit_code == 0
