import os
import sys

import pytest


def test_running_pytest(get_cli_invocation, project_dir):
    result = get_cli_invocation(
        sys.executable,
        '-m',
        'pytest',
        os.path.join(project_dir, 'tests'),
        '-vv',
        env={'PYTHONPATH': f'{str(os.path.join(project_dir, "src"))}'},
    )()
    assert result.exit_code == 0
    assert result.stderr == 'None'


@pytest.mark.integration
def test_running_tox(get_cli_invocation, project_dir):
    tox_ini_path = os.path.join(project_dir, 'tox.ini')
    assert os.path.isfile(tox_ini_path)

    tox_python_string = f'{sys.version_info.major}{sys.version_info.minor}'
    result = get_cli_invocation(
        sys.executable,
        '-m',
        'tox',
        '-c',
        os.path.join(project_dir, 'tox.ini'),
        '-e',
        'py{version}-dev'.format(version=tox_python_string),
        '-vv',
        env={'PYTHONPATH': f'{str(os.path.join(project_dir, "src"))}', 'PATH': ''},
    )()
    assert result.exit_code == 0
    assert result.stderr == 'None'
