import os
import sys


def test_running_pytest(
    get_cli_invocation,
    generate_project,
    test_project_generation_request,
):
    project_dir = generate_project(test_project_generation_request)
    result = get_cli_invocation(
        sys.executable,
        '-m',
        'pytest',
        os.path.join(project_dir, 'tests'),
        '-vv',
        env={
            'PYTHONPATH': f'{str(os.path.join(project_dir, "src"))}',
        })()
    assert result.exit_code == 0
    assert result.stderr == 'None'
