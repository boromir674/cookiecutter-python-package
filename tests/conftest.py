from __future__ import annotations
import os
import pytest
from typing import Callable, Any


@pytest.fixture
def production_template():
    import cookiecutter_python_package as cpp
    path = os.path.dirname(cpp.__file__)
    return path
    # MY_DIR = os.path.dirname(os.path.realpath(__file__))
    # TEST_DATA_DIR = os.path.join(MY_DIR, 'data')
    # return os.path.join(TEST_DATA_DIR, 'test_cookiecutter.json')


@pytest.fixture
def load_context_json():
    import json
    def _load_context_json(file_path: str) -> dict:
        with open(file_path, 'r') as fp:
            data = json.load(fp)
        return data
    return _load_context_json


@pytest.fixture
def test_context_file():
    MY_DIR = os.path.dirname(os.path.realpath(__file__))
    TEST_DATA_DIR = os.path.join(MY_DIR, 'data')
    return os.path.join(TEST_DATA_DIR, 'test_cookiecutter.json')


@pytest.fixture
def test_context(load_context_json, test_context_file):
    return load_context_json(test_context_file)


@pytest.fixture
def test_project_generation_request(production_template, test_context, tmpdir):
    return type('GenerationRequest', (), {
        'template': production_template,
        'destination': tmpdir,
        'default_dict': test_context,
    })


@pytest.fixture
def generate_project():
    from cookiecutter.main import cookiecutter
    def _generate_project(generate_request):
        return cookiecutter(
            generate_request.template,
            no_input=True,
            output_dir=generate_request.destination,
            overwrite_if_exists=True,
            default_config=generate_request.default_dict,
        )
    return _generate_project


# HELPERS
@pytest.fixture
def get_cli_invocation():
    import subprocess
    class CLIResult:
        exit_code: int
        stdout: str
        stderr: str
        def __init__(self, completed_process: subprocess.CompletedProcess):
            self.exit_code = int(completed_process.returncode)
            self.stdout = str(completed_process.stdout)
            self.stderr = str(completed_process.stderr)

        def __eq__(self, o) -> bool:
            equal_exit_code = self.exit_code == o.get('exit_code', self.exit_code)
            equal_stdout = self.stdout == o.get('stdout', self.stdout)
            equal_stderr = self.stderr == o.get('stderr', self.stderr)

            return equal_exit_code and equal_stdout and equal_stderr

    def get_callable(executable: str, *args, **kwargs) -> Callable[[], CLIResult]:
        def _callable() -> CLIResult:
            completed_process = subprocess.run(
                [executable] + list(args),
                env=kwargs.get('env', {}),
            )
            return CLIResult(completed_process)
        return _callable
    
    return get_callable


@pytest.fixture
def invoke_tox_cli_to_run_test_suite(get_cli_invocation):
    return get_cli_invocation('python', '-m', 'tox', '-vv')


# ASSERTIONS

@pytest.fixture
def assert_cli_passed():
    def _assert_cli_passed(runtime_result, expected_result):
        assert runtime_result == expected_result
    return _assert_cli_passed


