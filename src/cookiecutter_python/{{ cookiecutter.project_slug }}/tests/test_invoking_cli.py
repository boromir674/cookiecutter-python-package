import sys


def test_invoking_cli_as_python_module(run_subprocess):
    result = run_subprocess(
        sys.executable,
        '-m',
        '{{ cookiecutter.pkg_name }}',
        '--help',
    )
    assert result.exit_code == 0
    assert result.stderr == ''
    assert result.stdout.split('\n')[0] == "Usage: {{ cookiecutter.pkg_name|replace('_', '-') }} [OPTIONS]"
