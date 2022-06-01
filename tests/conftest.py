import os
import typing as t
from abc import ABC, abstractmethod

import attr
import pytest

my_dir = os.path.dirname(os.path.realpath(__file__))


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


@pytest.fixture
def production_template() -> str:
    import cookiecutter_python

    return os.path.dirname(cookiecutter_python.__file__)


@pytest.fixture
def load_context_json() -> t.Callable[[str], t.Dict]:
    import json

    def _load_context_json(file_path: str) -> t.Dict:
        with open(file_path, 'r') as fp:
            data = json.load(fp)
        return data

    return _load_context_json


@pytest.fixture
def test_context_file() -> str:
    return os.path.abspath(os.path.join(my_dir, 'data', 'test_cookiecutter.json'))


@pytest.fixture
def test_context(load_context_json, test_context_file) -> t.Dict:
    return load_context_json(test_context_file)


@pytest.fixture
def production_templated_project(production_template) -> str:
    return os.path.join(production_template, r'{{ cookiecutter.project_slug }}')


@attr.s(auto_attribs=True, kw_only=True)
class ProjectGenerationRequestData:
    template: str
    destination: str
    default_dict: bool
    extra_context: t.Optional[t.Dict[str, t.Any]]


@pytest.fixture
def test_project_generation_request(
    production_template, tmpdir
) -> ProjectGenerationRequestData:
    """Test data, holding information on how to invoke the cli for testing."""
    return ProjectGenerationRequestData(
        template=production_template,
        destination=tmpdir,
        default_dict=False,
        extra_context={
            'interpreters': {
                'supported-interpreters': [
                    '3.7',
                    '3.8',
                    '3.9',
                ]
            }
        },
    )


@pytest.fixture
def generate_project() -> t.Callable[[ProjectGenerationRequestData], str]:
    from cookiecutter_python.backend import cookiecutter

    def _generate_project(generate_request: ProjectGenerationRequestData) -> str:
        return cookiecutter(
            generate_request.template,
            no_input=True,
            extra_context=generate_request.extra_context,
            output_dir=generate_request.destination,
            overwrite_if_exists=True,
            # TODO: below takes a boolean variable!
            default_config=generate_request.default_dict,
        )

    return _generate_project


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
    assert all(['tox.ini' in x for x in (expected_files, runtime_files)])

    p = os.path.abspath(os.path.join(proj_dir, '.github', 'workflows', 'test.yaml'))
    print(p)
    with open(p, 'r') as f:
        contents = f.read()
    import re

    ver = r'"3\.(?:[6789]|10|11)"'
    # assert build matrix definition includes one or more python interpreters
    assert re.search(  # python-version: ["3.6", "3.7", "3.8", "3.9", "3.10"]
        fr'python-version:\s*\[\s*{ver}(?:(?:\s*,\s*{ver})*)\s*\]', contents
    )

    # assert that python interpreters are the expected ones given that we
    # invoke the 'generate_project' function:
    # no user yaml config & enabled the default_dict Flag!
    b = ', '.join(
        (
            f'"{int_ver}"'
            for int_ver in test_project_generation_request.extra_context['interpreters'][
                'supported-interpreters'
            ]
        )
    )
    assert f"python-version: [{b}]" in contents
    assert 'python-version: ["3.7", "3.8", "3.9"]' in contents
    return proj_dir


@pytest.fixture
def emulated_production_cookiecutter_dict(production_template, test_context) -> t.Mapping:
    """Equivalent to the {{ cookiecutter }} templated variable runtime value.

    Returns:
        t.Mapping: cookiecutter runtime configuration, as key/value hash map
    """
    import json
    from collections import OrderedDict

    with open(os.path.join(production_template, "cookiecutter.json"), "r") as fp:
        data: OrderedDict = json.load(fp, object_pairs_hook=OrderedDict)
        return OrderedDict(data, **test_context)


@pytest.fixture
def hook_request_class(emulated_production_cookiecutter_dict):
    @attr.s(auto_attribs=True, kw_only=True)
    class HookRequest:
        project_dir: t.Optional[str]
        # TODO improvement: add key/value types
        cookiecutter: t.Optional[t.Dict] = attr.ib(
            default=emulated_production_cookiecutter_dict
        )
        author: t.Optional[str] = attr.ib(default='Konstantinos Lampridis')
        author_email: t.Optional[str] = attr.ib(default='boromir674@hotmail.com')
        initialize_git_repo: t.Optional[bool] = attr.ib(default=True)
        interpreters: t.Optional[t.Dict] = attr.ib(
            default=[
                '3.6',
                '3.7',
                '3.8',
                '3.9',
                '3.10',
                '3.11',
            ]
        )
        module_name: t.Optional[str] = attr.ib(default='awesome_novelty_python_library')
        pypi_package: t.Optional[str] = attr.ib(
            default=attr.Factory(
                lambda self: self.module_name.replace('_', '-'), takes_self=True
            )
        )
        package_version_string: t.Optional[str] = attr.ib(default='0.0.1')

    return HookRequest


@pytest.fixture
def hook_request_new(hook_request_class):
    """Emulate the templated data used in the 'pre' and 'post' hooks scripts.

    Before and after the actual generation process (ie read the termplate files,
    generate the output files, etc), there 2 scripts that run. The 'pre' script
    (implemented as src/cookiecutter/hooks/pre_gen_project.py) and the 'post'
    script (implemented as src/cookiecutter/hooks/post_gen_project.py) run
    before and after the generation process respectively.

    These scripts are also templated! Consequently, similarly to the how the
    templated package depends on the 'templated variables', the 'pre' and 'post'
    scripts need a 'templating engine'.

    In our unit tests we do not run a 'templating engine' and thus it is
    required to mock the templated variables, when testing the 'pre' or 'post'
    script.

    This fixture provides an easily modified/extended infrastructure to mock all
    the necessary 'template variables' mentioned above.

    Thus, when writing (unit) test cases for testing code in the 'pre' or 'post'
    scripts (python modules) it is recommended to use this fixture to mock any
    'templated variables', according to your needs.

    Tip:
        Templated variables typically appear in double curly braces:
        ie {{ ... }}).
        If the 'code under test' depends on any 'template variable', (ie if you
        see code inside double curly braces), such as for example the common
        '{{ cookiecutter }}', then it is recommended to use this fixture to mock
        any required 'templated variable'.

    Returns:
        [type]: [description]
    """
    from software_patterns import SubclassRegistry

    class BaseHookRequest(metaclass=SubclassRegistry):
        pass

    @attr.s(auto_attribs=True, kw_only=True)
    @BaseHookRequest.register_as_subclass('pre')
    class PreGenProjectRequest(hook_request_class):
        project_dir: str = attr.ib(default=None)

    @BaseHookRequest.register_as_subclass('post')
    class PostGenProjectRequest(hook_request_class):
        pass

    return BaseHookRequest


@pytest.fixture
def request_factory(hook_request_new):
    def create_request_function(type_id: str):
        def _create_request(self, **kwargs):
            return hook_request_new.create(type_id, **kwargs)

        return _create_request

    return type(
        'RequestFactory',
        (),
        {
            'pre': create_request_function('pre'),
            'post': create_request_function('post'),
        },
    )()


@pytest.fixture
def get_check_pypi_mock():
    def build_check_pypi_mock_output(emulated_success=True):

        return type(
            'Future',
            (),
            {
                'result': lambda: type(
                    'HttpResponse',
                    (),
                    {
                        'status_code': 200 if emulated_success else 404,
                    },
                )
            },
        )()

    def _get_check_pypi_mock(
        emulated_success: t.Optional[bool] = True,
    ):
        def check_pypi_mock(*args, **kwargs):
            return (
                build_check_pypi_mock_output(emulated_success=emulated_success),
                'biskotaki',
            )

        return check_pypi_mock

    return _get_check_pypi_mock


PythonType = t.Union[bool, str, None]
CLIOverrideData = t.Optional[t.Dict[str, PythonType]]
CLIRunnerParameters = t.Tuple[t.Sequence[str], t.Dict[str, t.Any]]


@pytest.fixture
def cli_invoker_params() -> t.Callable[[t.Any], CLIRunnerParameters]:
    """Create parameters for running a test that invokes a cli program.

    Use to generate the cli (string) arguments (positional and optional), as
    well other optional information to be passed into a 'cli test invocation'
    function.

    Get a list of objects that can be passed in the `generate` function.

    Returns a callable that upon invocation creates a list of objects suitable
    for passing into the `generate` method. The callable accepts **kwargs that
    allow to provide values to override the defaults.

    Returns:
        callable: the callable that creates `generate` arguments lists
    """
    from collections import OrderedDict
    from copy import deepcopy

    class Args:
        args = [  # these flags and default values emulate the 'generate-python'
            # cli (exception is the '--config-file' flag where we pass the
            # biskotaki yaml by default, instead of None)
            ('--no-input', False),
            ('--checkout', False),
            ('--verbose', False),
            ('--replay', False),
            ('--overwrite', False),
            ('--output-dir', '.'),
            (
                '--config-file',  # biskotaki yaml as default instead of None
                os.path.abspath(os.path.join(my_dir, '..', '.github', 'biskotaki.yaml')),
            ),
            ('--default-config', False),
            ('--directory', None),
            ('--skip-if-file-exists', False),
        ]

        def __init__(self, args_with_default: CLIOverrideData = None, **kwargs) -> None:
            self.cli_defaults = OrderedDict(Args.args)

            if args_with_default is None:
                self.map = deepcopy(self.cli_defaults)
            else:
                assert all([k in self.cli_defaults for k in args_with_default])
                self.map = OrderedDict(self.cli_defaults, **dict(args_with_default))
            assert (
                [k for k in self.map]
                == [k for k, _ in Args.args]
                == [k for k in self.cli_defaults]
            )

        def __iter__(self) -> t.Iterator[str]:
            for cli_arg, default_value in self.map.items():
                if bool(default_value):
                    yield cli_arg
                    if type(self.cli_defaults[cli_arg]) != bool:
                        yield str(default_value)

    def parameters(
        optional_cli_args: CLIOverrideData = None,
    ) -> CLIRunnerParameters:
        """Generate parameters for running a test that invokes a cli program.

        Parameters of a test that invokes a cli program are distinguished in two
        types:

        - the actual cli parameters, as a list of strings
            these would function the same as if the program was invoked in a
            shell script or in an interactive console/terminal.
        - optional information to be passed to the cli invoker as required
            per test case, as **kwargs

        Generate, positional and/or optional (ie flags) cli arguments.

        Input kwargs can be used to overide the default values for the flags
        specified in class Args (see above).

        Args:
            optional_cli_args (CLIOverrideData, optional): cli optional
                arguments to override. Defaults to None.

        Returns:
            t.Tuple[t.Sequence[str], t.Dict]: the requested cli invoker test
                parameters
        """
        return list(Args(args_with_default=optional_cli_args)), {}

    return parameters


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

    def get_callable(executable: str, *args, **kwargs) -> t.Callable[[], AbstractCLIResult]:
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

        def __call__(self, object_ref: Any, attribute: str) -> Any:
            object_reference = getattr(object_ref, attribute)
            if object_reference is None:
                raise RuntimeError(self.debug_message_factory(object_ref, attribute))
            return object_reference

    return AttributeGetter


@pytest.fixture
def generic_object_getter_class(attribute_getter, monkeypatch):
    """Class instances can extract a requested object from within a module and optionally patch any object in the module's namespace at runtime."""
    from importlib import import_module
    from typing import Any, Generic, TypeVar

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
            return self._attr_getter(object_module, self._extract_object_symbol_name(request))

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
def get_object(object_getter_class):
    """Import an object from a module and optionally mock any object in its namespace.

    A callable that can import an object, given a reference (str), from a module
    , given its "path" (string represented as 'dotted' modules: same way python
    code imports modules), and provide the capability to monkeypatch/mock any
    object found in the module's namespace at runtime.

    The client code must supply the first 2 arguments at runtime, correspoding
    to the object's symbol name (str) and module "path" (str).

    The client code can optionally use the 'overrides' kwarg to supply a python
    dictionary to specify what runtime objects to mock and how.

    Each dictionary entry should model your intention to monkeypatch one of the
    module namespace' objects with a custom 'mock' value.

    Each dictionary key should be a string corresponding to an object's
    reference name (present in the module's namespace) and each value should be
    a callable that can construct the 'mock' value.
    The callable should take no arguments and acts as a "factory", that when
    called should provide the 'mock' value.

    Example:

        def mocked_request_get()
        business_method = get_object(
            "business_method",
            "business_package.methods",
            overrides={"production": lambda: 'mocked'}
        )

    Args:
        symbol (str): the object's reference name
        module (str): the module 'path' represented as module names "joined" by
            "." (dots)
        overrides (dict, optional): declare what to monkeypatch and with what "mocks". Defaults to None.

    Returns:
        Any: the object imported from the module with its namespace potentially mocked
    """

    class ObjectGetterAdapter(object_getter_class):
        """Adapter Class of the ObjectGetter class, see object_getter_class fixture.

        Returns:
            ObjectGetterAdapter: the Adapter Class
        """

        def __call__(self, symbol_ref: str, module: str, **kwargs):
            return super().__call__(
                type(
                    "RequestLike",
                    (),
                    {"symbol_name": symbol_ref, "object_module_string": module},
                ),
                **kwargs,
                # overrides=kwargs.get('overrides', {})
            )

    return ObjectGetterAdapter()
