import os
import pytest
from typing import Callable, Any
from abc import ABC, abstractmethod


class AbstractCLIResult(ABC):

    @property
    @abstractmethod
    def exit_code(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def stdout(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def stderr(self) -> str:
        raise NotImplementedError

    def __eq__(self, o) -> bool:
        equal_exit_code = self.exit_code == o.get('exit_code', self.exit_code)
        equal_stdout = self.stdout == o.get('stdout', self.stdout)
        equal_stderr = self.stderr == o.get('stderr', self.stderr)

        return equal_exit_code and equal_stdout and equal_stderr



@pytest.fixture
def production_template():
    import cookiecutter_python as cpp
    path = os.path.dirname(cpp.__file__)
    return path


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
    class CLIResult(AbstractCLIResult):
        exit_code: int
        stdout: str
        stderr: str
        def __init__(self, completed_process: subprocess.CompletedProcess):
            self._exit_code = int(completed_process.returncode)
            self._stdout = str(completed_process.stdout)
            self._stderr = str(completed_process.stderr)
        @property
        def exit_code(self) -> int:
            return self._exit_code
        @property
        def stdout(self) -> str:
            return self._stdout
        @property
        def stderr(self) -> str:
            return self._stderr
    def get_callable(executable: str, *args, **kwargs) -> Callable[[], AbstractCLIResult]:
        def _callable() -> AbstractCLIResult:
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
