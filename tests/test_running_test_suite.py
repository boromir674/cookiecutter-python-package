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
                **{
                    'LC_ALL': 'C.UTF-8',
                    'LANG': 'C.UTF-8',
                },
            )
        if sys.platform == 'darwin':  # ie we are on a Mac OS
            return dict(
                environment_variables,
                **{
                    'LC_ALL': 'en_GB.UTF-8',
                    'LANG': 'en_GB.UTF-8',
                },
            )
        if sys.platform == 'win32':  # ie we are on a Windows OS
            return dict(
                environment_variables,
                **{
                    'LC_ALL': 'C.UTF-8',
                    'LANG': 'C.UTF-8',
                },
            )
        raise RuntimeError(f'Unexpected System Found: {sys.platform}')

    return get_environment_variables


def test_running_pytest(environment, get_cli_invocation, project_dir):
    result = get_cli_invocation(
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
    print('\n----- DEBUGGING Pytest Invocation Unit Test ------\n')
    print(result.stdout)
    print('\n END DEBUG ------------------')
    assert ' failed' not in result.stdout
    assert result.stderr == ''
    assert result.exit_code == 0
