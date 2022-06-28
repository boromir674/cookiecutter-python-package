import sys
import typing as t
import pytest


@pytest.fixture
def get_cli_invocation():
    import subprocess
    import sys

    class CLIResult:
        exit_code: int
        stdout: str
        stderr: str

        def __init__(self, completed_process: subprocess.CompletedProcess):
            self._exit_code = int(completed_process.returncode)
            self._stdout = str(completed_process.stdout, encoding='utf-8')
            self._stderr = str(completed_process.stderr, encoding='utf-8')

        @property
        def exit_code(self) -> int:
            return self._exit_code

        @property
        def stdout(self) -> str:
            return self._stdout

        @property
        def stderr(self) -> str:
            return self._stderr

    def python37_n_above_kwargs():
        return dict(
            capture_output=True,  # capture stdout and stderr separately
            check=True,
        )

    def python36_n_below_kwargs():
        return dict(
            stdout=subprocess.PIPE,  # capture stdout and stderr separately
            stderr=subprocess.PIPE,
            check=True,
        )

    subprocess_run_map = {
        True: python36_n_below_kwargs,
        False: python37_n_above_kwargs,
    }

    def get_callable(cli_args: t.List[str], **kwargs) -> t.Callable[[], CLIResult]:
        def subprocess_run() -> CLIResult:
            kwargs_dict = subprocess_run_map[sys.version_info < (3, 7)]()
            completed_process = subprocess.run(cli_args, **dict(kwargs_dict, **kwargs))
            return CLIResult(completed_process)

        return subprocess_run

    def execute_command_in_subprocess(executable: str, *args, **kwargs):
        execute_subprocess = get_callable([executable] + list(args), **kwargs)
        return execute_subprocess()

    return execute_command_in_subprocess


def test_invoking_cli_as_python_module(get_cli_invocation):
    result = get_cli_invocation(
        sys.executable,
        '-m',
        '{{ cookiecutter.pkg_name }}',
        '--help',
    )
    assert result.exit_code == 0
    assert result.stderr == ''
    assert result.stdout.split('\n')[0] == "Usage: {{ cookiecutter.pkg_name|replace('_', '-') }} [OPTIONS]"
