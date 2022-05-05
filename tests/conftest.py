import os
from typing import Callable
from abc import ABC, abstractmethod

import pytest
from software_patterns import SubclassRegistry


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
def test_context(load_context_json, test_context_file) -> dict:
    return load_context_json(test_context_file)


@pytest.fixture
def test_project_generation_request(production_template, test_context, tmpdir):
    return type(
        'GenerationRequest',
        (),
        {
            'template': production_template,
            'destination': tmpdir,
            'default_dict': test_context,
        },
    )


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


@pytest.fixture
def production_templated_project(production_template):
    return os.path.join(production_template, r'{{ cookiecutter.project_slug }}')


@pytest.fixture
def project_dir(
    generate_project, test_project_generation_request, production_templated_project
):
    """Generate a Fresh new Project using the production cookiecutter template and
    the tests/data/test_cookiecutter.json file as default dict."""
    proj_dir: str = generate_project(test_project_generation_request)
    runtime_files = os.listdir(proj_dir)
    # we add '.git' since the project we generate for testing purposes
    # uses a 'test_context' that instructs cookiecutter to initialiaze a git
    # repo (see post_gen_project.py hook)
    expected_files = os.listdir(production_templated_project) + ['.git']
    assert set(expected_files) == set(runtime_files)
    assert len(expected_files) == len(runtime_files)
    return proj_dir


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

    def get_callable(
        executable: str, *args, **kwargs
    ) -> Callable[[], AbstractCLIResult]:
        def _callable() -> AbstractCLIResult:
            completed_process = subprocess.run(
                [executable] + list(args), env=kwargs.get('env', {})
            )
            return CLIResult(completed_process)

        return _callable

    return get_callable


@pytest.fixture
def invoke_tox_cli_to_run_test_suite(get_cli_invocation):
    return get_cli_invocation('python', '-m', 'tox', '-vv')


@pytest.fixture
def attribute_getter():
    from typing import Any

    class AttributeGetter(object):
        def __init__(self, debug_message_factory):
            self.debug_message_factory = debug_message_factory

        def get(self, object_ref: Any, attribute: str) -> Any:
            object_reference = getattr(object_ref, attribute)
            if object_reference is None:
                raise RuntimeError(self.debug_message_factory(object_ref, attribute))
            return object_reference

    return AttributeGetter


@pytest.fixture
def generic_object_getter_class(attribute_getter, monkeypatch):
    """Class instances can extract a requested object from within a module and optionally patch any object in the module's namespace at runtime."""
    from typing import Any, Generic, TypeVar
    from importlib import import_module

    T = TypeVar('T')

    class AbstractGenericObjectGetter(Generic[T]):
        def __init__(self, debug_message=None):
            # if True we want to patch one or more objects, found in the same module's namespace as the object that is requested at runtime
            # if False we want the object as it is computed in the production code

            self._get_object_callback = {
                True: self._get_production_object,
                False: self._build_object,
            }
            if debug_message:
                self._attr_getter = attribute_getter(
                    lambda _object, name: "{msg}. Did not find {name} on object of type {type}".format(
                        msg=debug_message, name=name, type=type(_object).__name__
                    )
                )
            else:
                self._attr_getter = attribute_getter(
                    lambda _object, name: "Did not find {name} on object of type {type}".format(
                        name=name, type=type(_object).__name__
                    )
                )

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            return self.get(*args, **kwargs)

        def get(self, request: T, overrides={}):
            # use_production_object: bool = not self._bool_key({'overrides': overrides})
            d = {'overrides': overrides}
            use_production_object: bool = not bool(d.get('overrides'))
            return self._get_object_callback[use_production_object](request, **d)

        def _get_production_object(self, request: T, **kwargs):
            object_module = self._get_object_module(request)
            computed_object = self._get_object(request, object_module)
            return computed_object

        def _build_object(self, request: T, overrides={}):
            object_module = self._get_object_module(request)
            for symbol_name, factory in overrides.items():
                monkeypatch.setattr(object_module, symbol_name, factory())
            computed_object = self._get_object(request, object_module)
            return computed_object

        def _get_object_module(self, request: T):
            return import_module(self._extract_module_string(request))

        def _extract_module_string(self, request: T) -> str:
            """Extract the module 'path' from the request as dot (.) separated words (module/subpackages names)."""
            raise NotImplementedError

        def _extract_object_symbol_name(self, request: T) -> str:
            """Extract the name of the reference (symbol in code) that points to the object requested for getting at runtime."""
            raise NotImplementedError

        def _get_object(self, request: T, object_module):
            return self._attr_getter(
                object_module, self._extract_object_symbol_name(request)
            )

    return AbstractGenericObjectGetter


@pytest.fixture
def object_getter_class(generic_object_getter_class):
    """Do a dynamic import of a module and get an object from its namespace.

    This fixture returns a Python Class that can do a dynamic import of a module
    and get an object from its namespace.

    Instances of this class are callable's (they implement the __call__ protocol
    ) and uppon calling the return a reference to the object "fetched" from the
    namespace.

    Callable instances arguments:
    * 1st: object with the 'symbol_namel': str and 'object_module_string': str
        attributes expected "on it"

    Returns:
        ObjectGetter: Class that can do a dynamic import and get an object
    """
    from abc import ABC, abstractmethod

    class RequestLike(ABC):
        @property
        @abstractmethod
        def symbol_name(self) -> str:
            # how the object (ie a get_job method) is imported into the namespace of a module (ie a metadata_provider module)
            raise NotImplementedError

        @property
        @abstractmethod
        def object_module_string(self) -> str:
            # the module (in a \w+\.\w+\.\w+ kind of format) where the object reference is present/computed
            raise NotImplementedError

    class ObjectGetter(generic_object_getter_class[RequestLike]):
        def _extract_module_string(self, request) -> str:
            return request.object_module_string

        def _extract_object_symbol_name(self, request) -> str:
            return request.symbol_name

    return ObjectGetter


@pytest.fixture
def object_getter_adapter_class(object_getter_class):
    """Adapter Class of the ObjectGetter class, see object_getter_class fixture.

    Returns:
        ObjectGetterAdapter: the Adapter Class
    """

    class ObjectGetterAdapter(object_getter_class):
        def __call__(self, symbol_ref: str, module: str, **kwargs):
            return super().__call__(
                type(
                    'RequestLike',
                    (),
                    {'symbol_name': symbol_ref, 'object_module_string': module},
                ),
                **kwargs,
                # overrides=kwargs.get('overrides', {})
            )

    return ObjectGetterAdapter


@pytest.fixture
def get_object(object_getter_adapter_class):
    return object_getter_adapter_class()


@pytest.fixture
def hook_request():
    def __init__(self, **kwargs):
        self.module_name = kwargs.get('module_name', 'awesome_novelty_python_library')
        self.pypi_package = kwargs.get(
            'pypi_package', self.module_name.replace('_', '-')
        )
        self.package_version_string = kwargs.get('package_version_string', '0.0.1')

    return type('PreGenProjectRequest', (), {'__init__': __init__})


@pytest.fixture
def emulated_production_cookiecutter_dict(production_template, test_context):
    import json

    with open(os.path.join(production_template, 'cookiecutter.json'), 'r') as fp:
        return dict(json.load(fp), **test_context)


@pytest.fixture
def hook_request_new(emulated_production_cookiecutter_dict):
    class HookRequest(object):
        pass

    class BaseHookRequest(metaclass=SubclassRegistry):
        pass

    @BaseHookRequest.register_as_subclass('pre')
    class PreGenProjectRequest(HookRequest):
        def __init__(self, **kwargs):
            self.module_name = kwargs.get(
                'module_name', 'awesome_novelty_python_library'
            )
            self.pypi_package = kwargs.get(
                'pypi_package', self.module_name.replace('_', '-')
            )
            self.package_version_string = kwargs.get('package_version_string', '0.0.1')

    @BaseHookRequest.register_as_subclass('post')
    class PostGenProjectRequest(HookRequest):
        def __init__(self, **kwargs):
            self.project_dir = kwargs['project_dir']
            self.cookiecutter = kwargs.get(
                'cookiecutter', emulated_production_cookiecutter_dict
            )
            self.author = kwargs.get('author', 'Konstantinos Lampridis')
            self.author_email = kwargs.get('author_email', 'boromir674@hotmail.com')
            self.initialize_git_repo = kwargs.get('initialize_git_repo', True)

    return type(
        'RequestInfra', (), {'class_ref': HookRequest, 'registry': BaseHookRequest}
    )


@pytest.fixture
def request_factory(hook_request_new):
    def create_request_callback(type_id: str):
        def _create_request(**kwargs):
            return hook_request_new.registry.create(type_id, **kwargs)

        return _create_request

    return type(
        'RequestFactory',
        (),
        {
            'pre': create_request_callback('pre'),
            'post': create_request_callback('post'),
        },
    )
