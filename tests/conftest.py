import os
import sys
import typing as t

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

from pathlib import Path

import attr
import pytest

my_dir: str = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def test_root() -> Path:
    """Root directory Path of the test suite; ie /projects/my-project/tests/"""
    return Path(my_dir)


@pytest.fixture
def distro_loc() -> Path:
    """Get Installation Root Directory; ie /python/site-packages/cookiecutter_python"

    This is the root directory of the Python Package Distribution (PPD).

    Returns:
        Path: the root directory of the Python Package Distribution (PPD).
    """
    import cookiecutter_python

    # if top-level init is at '/site-packages/cookiecutter_python/__init__.py'
    # then distro_path is '/site-packages/cookiecutter_python'
    distro_path: Path = Path(cookiecutter_python.__file__).parent

    # BTD is compatible to Generator's Templating Engine, i.e. Cookiecutter (jinja2)
    # THEN the TD includes valid Template Variables Configuration
    ## REGRESSION Tests ##
    assert (distro_path / 'cookiecutter.json').is_file(), f"distro_path: {distro_path}"
    assert (
        distro_path / r'{{ cookiecutter.project_slug }}'
    ).is_dir(), f"distro_path: {distro_path}"
    # hard require pyproject.toml for at Python Repo root dir
    assert (
        distro_path / r'{{ cookiecutter.project_slug }}' / 'pyproject.toml'
    ).is_file(), f"distro_path: {distro_path}"
    return distro_path


class ProjectGenerationRequestDataProtocol(Protocol):
    template: str
    destination: str
    default_dict: bool
    extra_context: t.Optional[t.Dict[str, t.Any]]


@pytest.fixture
def generate_project() -> t.Callable[[ProjectGenerationRequestDataProtocol], str]:
    """Generator backend used by the production Generator CLI."""
    from cookiecutter_python.backend.generator import generator as cookiecutter

    def _generate_project(generate_request: ProjectGenerationRequestDataProtocol) -> str:
        assert isinstance(
            generate_request.template, str
        ), f"Expexted str for template, got {type(generate_request.template)}"
        return cookiecutter(
            generate_request.template,
            no_input=True,
            extra_context=generate_request.extra_context,
            output_dir=generate_request.destination,
            overwrite_if_exists=True,
            default_config=generate_request.default_dict,
        )

    return _generate_project


@pytest.fixture
def project_dir(generate_project, distro_loc, tmpdir):
    """Generate a Fresh new Project using the production cookiecutter template and
    the tests/data/test_cookiecutter.json file as default dict."""

    @attr.s(auto_attribs=True, kw_only=True)
    class ProjectGenerationRequestData:
        """Information to pass in the CLI when invoked for testing purposes."""

        template: str
        destination: str
        default_dict: bool
        extra_context: t.Optional[t.Dict[str, t.Any]]

    proj_dir: str = generate_project(
        ProjectGenerationRequestData(
            template=str(distro_loc),
            destination=tmpdir,
            default_dict=False,
            extra_context={
                'project_type': 'module+cli',
                'interpreters': {
                    'supported-interpreters': [
                        '3.7',
                        '3.8',
                        '3.9',
                    ]
                },
            },
        )
    )
    return proj_dir


@pytest.fixture
def hook_request_new(distro_loc):
    """Emulate the templated data used in the 'pre' and 'post' hooks scripts.

    MUST be kept in SYNC with the 'pre' and 'post' hook scripts, and their
    interface.

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
    import json
    from collections import OrderedDict

    from software_patterns import SubclassRegistry

    # Read JSON data from 'tests/data/test_cookiecutter.json'
    # The JSON schema and values MUST reflect a valid internal state of the
    # Generator's Template Engine.
    # at the moment, we exclusively use cookiecutter (and jinja2) for templating
    # GIVEN data that reflect a state, which the Templating Engine is possible
    # to arrive at, when the Generator CLI is invoked.
    ### We want to skip running the templating engine, so we mock the state
    ### that the templating engine would have produced.
    engine_state: OrderedDict = json.loads(
        (Path(my_dir) / 'data' / 'test_cookiecutter.json').read_text(),
        object_pairs_hook=OrderedDict,
    )

    # THEN the state must be a valid Context for the Template Engine
    assert set(engine_state.keys()) == {'cookiecutter'}
    intended_template_path: str = engine_state['cookiecutter'].pop('_template')
    assert intended_template_path == '.'

    assert '_template' not in engine_state['cookiecutter'].keys()

    # GIVEN the Generator's Templated Variables Configuration file (ie cookiecutter.json)
    # which is used at runtime, when the Generator CLI is invoked, and thus if
    # file changes, the Generator's behaviour changes.
    td_cookiecutter_json_data = json.loads(
        (distro_loc / 'cookiecutter.json').read_text(), object_pairs_hook=OrderedDict
    )

    # ΤΗΕΝ engine_state (excluding _template) must be supported TD cookiecutter.json
    intended_templated_variables: t.Set[str] = set(engine_state['cookiecutter'].keys())
    supported_template_variables: t.Set[str] = set(td_cookiecutter_json_data.keys())
    engine_state_vars_supported_by_td: bool = intended_templated_variables.issubset(
        supported_template_variables
    )
    assert engine_state_vars_supported_by_td

    # WHEN we define a way to create a valid input for pre and post hooks
    @attr.s(auto_attribs=True, kw_only=True)
    class HookRequest:
        """Hook Request Data Class.

        This class is used to mock the 'templated variables' that are used in
        the 'pre' and 'post' scripts.

        The 'pre' and 'post' scripts are also templated! Consequently, similarly
        to the how the templated package depends on the 'templated variables',
        the 'pre' and 'post' scripts need a 'templating engine'.

        In our unit tests we do not run a 'templating engine' and thus it is
        required to mock the templated variables, when testing the 'pre' or
        'post' script.

        This class provides an easily modified/extended infrastructure to mock
        all the necessary 'template variables' mentioned above.

        Thus, when writing (unit) test cases for testing code in the 'pre' or
        'post' scripts (python modules) it is recommended to use this class to
        mock any 'templated variables', according to your needs.

        Args:
            project_dir (t.Optional[str]): [description]
            cookiecutter (t.Optional[t.Dict]): [description]
            author (t.Optional[str]): [description]
            author_email (t.Optional[str]): [description]
            initialize_git_repo (t.Optional[bool]): [description]
            interpreters (t.Optional[t.Dict]): [description]
            project_type (t.Optional[str]): [description]
            module_name (t.Optional[str]): [description]
        """

        project_dir: t.Optional[str]
        # TODO improvement: add key/value types
        ### We want to skip running the templating engine, so we mock the state
        ### that the templating engine would have produced.

        # Templated Vars (cookiecutter) use in Context for Jinja Rendering
        vars: t.Optional[t.Dict] = attr.ib(
            default=OrderedDict(td_cookiecutter_json_data, **engine_state['cookiecutter'])
        )
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
        project_type: t.Optional[str] = attr.ib(default='module')
        module_name: t.Optional[str] = attr.ib(default='awesome_novelty_python_library')
        pypi_package: t.Optional[str] = attr.ib(
            default=attr.Factory(
                lambda self: self.module_name.replace('_', '-'), takes_self=True
            )
        )
        package_version_string: t.Optional[str] = attr.ib(default='0.0.1')
        docs_extra_info: t.Optional[bool] = attr.ib(
            default=dict(
                **{'mkdocs': 'docs-mkdocs', 'sphinx': 'docs-sphinx'},
            )
        )
        docs_website: t.Optional[t.Dict[str, str]] = attr.ib(
            default={
                'builder': 'sphinx',
                'python_runtime': '3.10',
            }
        )

        def __attrs_post_init__(self):
            self.vars['project_type'] = self.project_type

    class BaseHookRequest(metaclass=SubclassRegistry):
        pass

    @attr.s(auto_attribs=True, kw_only=True)
    @BaseHookRequest.register_as_subclass('pre')
    class PreGenProjectRequest(HookRequest):
        project_dir: str = attr.ib(default=None)

    @BaseHookRequest.register_as_subclass('post')
    class PostGenProjectRequest(HookRequest):
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
def mock_hosting_services(future_session_mock):
    """Mock the FuturesSession class given urls and http status codes.

    Mocks the FuturesSession class given urls and the desired emulated status
    codes that the remote web server supposedly responds with.

    Args:
        url_2_code (Mapping): mapping of url strings to status code integers
    """
    from typing import Any

    def _futures_session_mock_class(url_2_code):
        class FutureSessionMockAdapter:
            future_session_mock_instance: Any
            _instance = None

            def __new__(cls):
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    # create a mock instance of the FuturesSession class
                    # atm, the is LIMITED to supply only 'get' method
                    # when mock `get` is called, it immediately returns an Futere HTTPResponse-like
                    # which provides the 'result' attribute, which can immediately be evaluated.
                    # Ref: self.result = lambda: type('HttpResponseMock', (), {'status_code': status_code})
                    cls._instance.future_session_mock_instance = future_session_mock(
                        url_2_code
                    )
                    # when 'get' method is called, the insted of real futures behavior
                    # our mock will be called instead, which immediately returns
                    # an object, which provides the 'result' attribute, which can
                    # immediately be evaluated.

                    # Ref: self.result = lambda: type('HttpResponseMock', (), {'status_code': status_code})

                return cls._instance

            def get(self, url: str):
                return self.future_session_mock_instance.get(url)

            @property
            def url_2_code(self):
                return self.future_session_mock_instance.url_2_code

        return FutureSessionMockAdapter

    return _futures_session_mock_class


@pytest.fixture
def mock_check(get_object, mock_hosting_services):
    from typing import Any

    import attr

    from cookiecutter_python.backend.hosting_services.web_hosting_service import (
        HostingServices,
    )

    @attr.s(auto_attribs=True, slots=True)
    class MockCheck:
        _config: Any = attr.ib(default=None)
        futures_session_instance_mock: Any = attr.ib(init=False)  # singleton instance
        hosting_service_infos: t.MutableMapping[str, t.Any] = attr.ib(
            init=False, default=attr.Factory(dict)
        )

        def __attrs_post_init__(self):
            self.mock_futures_session()

        @property
        def config(self):
            return self._config

        @config.setter
        def config(self, config):
            self._config = config

        def mock_futures_session(self):
            # GIVEN a class that can act in place of the FuturesSession class
            # NOTE: instances of class can only mock the 'get' method
            futures_session_class_mock = mock_hosting_services({})
            # we let client call the __call__ method of this instance to
            # in order to setup the url_2_code dict with actual values

            # because futures_session_class_mock is implemented as singleton
            # we create a new instance of it, to
            self.futures_session_instance_mock = futures_session_class_mock()
            # has 'get' method amd 'url_2_code' property
            get_object(
                'WebHostingServiceChecker',
                'cookiecutter_python.backend.hosting_services.check_web_hosting_service',
                # we monkeypatch the FuturesSession class to return our mock
                overrides={'FuturesSession': lambda: futures_session_class_mock},
            )
            # EFFECT:
            # when client code invokes the __call__ method of a WebHostingServiceChecker isntance obj
            # then 1. will create a session, not (as in prod) as an instance of FuturesSession class,
            # but as an instance of our mock class (singleton)
            # 2. will call the 'get' method of our mock session (not the prod instance method of FuturesSession class)
            # which immediately returns an future-instance-like object (in place of prod future instance),
            # which provides the 'result' attribute, which can immediately be evaluated.
            # 3. will return a "request'Result', with same interface as prod, which
            # instead of wrapping a real future instance (like in prod),
            # it wraps our future-instance-like mock object

        def __call__(self, service_name: str, found: bool):
            # Find URL from service_name
            if service_name not in self.hosting_service_infos:
                # A HostingService instance reports the corresponding Template Variable
                # with property 'variable_name' (ie 'readthedocs_project_slug', 'pkg_name')
                self.hosting_service_infos[str(service_name)] = HostingServices.create(
                    service_name
                )
            info = self.hosting_service_infos[service_name]
            url = info.service.url(
                self._config.data.get(
                    info.variable_name,
                    "cannot determine 'name' (ie pypi, readthedocs) from config file",
                )
            )
            # Emulate singal emitted by the WebHostingServiceChecker
            self.futures_session_instance_mock.url_2_code[url] = 200 if found else 404

    return MockCheck()


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
        args = [
            # these flags and default values emulate the 'generate-python' cli
            ('--no-input', False),
            ('--checkout', False),
            ('--verbose', False),
            ('--replay', False),
            ('--overwrite', False),
            ('--output-dir', '.'),
            ('--config-file', None),
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
                    if not isinstance(self.cli_defaults[cli_arg], bool):
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


# keep in Sync with user_config Fixture, if Type Check fails
class ConfigProtocol(Protocol):
    data: t.Mapping


ConfigInterface = t.TypeVar('ConfigInterface')


class ConfigInterfaceGeneric(t.Generic[ConfigInterface]):
    def __getitem__(self, file_path_str: t.Union[str, None]) -> ConfigInterface: ...


@pytest.fixture
def user_config(distro_loc: Path) -> ConfigInterfaceGeneric[ConfigProtocol]:
    """Context Values Interface, derived either from User's YAML or Default JSON

    Args:
        distro_loc (Path): [description]

    Returns:
        [type]: [description]
    """ """"""
    import json
    from pathlib import Path

    from cookiecutter_python.backend.load_config import load_yaml as prod_load_yaml

    # Types
    PathLike = t.Union[str, bytes, os.PathLike]
    DataLoader = t.Callable[[t.Union[str, Path]], t.MutableMapping]

    # Support Data
    def _load_context_json(file_path: PathLike) -> t.Dict:
        with open(file_path, 'r') as fp:
            data = json.load(fp)
        return data

    _prod_yaml_loader: t.Callable[[PathLike], t.MutableMapping] = prod_load_yaml
    # Aliases, for shortcuts
    config_files = {
        'biskotaki': '.github/biskotaki.yaml',
        'without-interpreters': 'tests/data/biskotaki-without-interpreters.yaml',
    }

    @attr.s(auto_attribs=True, slots=True)
    class ConfigData:
        """Compute the 'default parameters' either from user yaml or from json.

        The 'default parameters' are the parameters that are used to generate
        the project. In interactive mode the user is prompted to provide values
        or the default values are used.

        If path is given then it is assumed that a 'user config' yaml file has
        been passed.

        If path is None, then it is assumed that no 'user config' yaml file has
        been passed and thus the 'default parameters' will be computed using the
        cookiecutter.json. The 'default parameters', in this case, are emulated
        to imitate the possible jinja2 transformations that may be defined in
        each of the cookiecutter.json files.

        Args:
            Union[str, None]: the path to the user config yaml file or None
        """

        path: t.Union[str, None]

        _data_file_path: t.Union[str, Path, None] = attr.ib(init=False, default=None)
        _config_file_arg: t.Optional[str] = attr.ib(init=False, default=None)
        _loader: DataLoader = attr.ib(init=False)
        _data: t.Mapping = attr.ib(init=False)

        def __attrs_post_init__(self):
            if self.path is not None:
                # Read data coming from yaml
                data_file = Path(my_dir) / '..' / config_files.get(self.path, self.path)
                assert data_file.exists()
                assert data_file.is_file()
                assert data_file.suffix in (
                    '.yaml',
                    '.yml',
                ), f"Invalid user config file {data_file}. Expected .yaml or .yml extension."

                self._config_file_arg = data_file
                self._data_file_path = data_file
                self._loader = ConfigData.load_yaml(_prod_yaml_loader)
            else:
                self._config_file_arg = None
                self._data_file_path = distro_loc / 'cookiecutter.json'

                assert self._data_file_path.exists()
                assert self._data_file_path.is_file()
                assert (
                    self._data_file_path.suffix == '.json'
                ), f"Invalid cookiecutter.json file {self._data_file_path}. Expected .json extension."
                self._loader = ConfigData.load_json(_load_context_json)

            self._data = self._loader(self._data_file_path)

        @property
        def data(self) -> t.Mapping:
            """Get the computed 'default parameters' as standard python objects.

            Returns:
                t.Mapping: the 'default parameters' as standard python objects
            """
            return self._data

        @staticmethod
        def load_json(loader: DataLoader):
            def _load_json(json_file: str):
                data = loader(json_file)
                data['project_slug'] = data['project_name'].lower().replace(' ', '-')
                data['docker_image'] = data['project_slug']
                data['project_type'] = data['project_type'][0]
                data['pkg_name'] = data['project_name'].lower().replace(' ', '_')
                data['author'] = data['full_name']
                data['initialize_git_repo'] = {'yes': True}.get(
                    data['initialize_git_repo'][0], False
                )
                # Docs Building #
                data['docs_builder'] = data['docs_builder'][0]  # choice variable
                # RTD CI Python Version #
                data['rtd_python_version'] = data['rtd_python_version'][0]  # choice variable
                return data

            return _load_json

        @staticmethod
        def load_yaml(loader: DataLoader):
            def _load_yaml(yaml_file: str):
                data = loader(yaml_file)['default_context']
                data['initialize_git_repo'] = {'yes': True}.get(
                    data['initialize_git_repo'], False
                )
                return data

            return _load_yaml

        @property
        def project_slug(self) -> str:
            return self._data['project_slug']

        @property
        def config_file(self) -> t.Union[str, None]:
            return self._config_file_arg

    return type(
        'ConfigFile',
        (),
        {
            '__getitem__': lambda self, item: ConfigData(
                item,
            )
        },
    )()


class RelativePathsGenerator(Protocol):
    """Generate relative paths from a given root folder."""

    def relative_file_paths(self) -> t.Iterator[Path]: ...


@pytest.fixture
def project_files() -> t.Callable[[t.Union[str, Path]], RelativePathsGenerator]:
    """Files of a generated Project, as iterable of file paths (excluding dirs)."""
    from glob import glob
    from os import path
    from pathlib import Path

    import attr

    @attr.s(auto_attribs=True, slots=True, frozen=True)
    class ProjectFiles:
        root_dir: t.Union[str, Path]

        _glob: t.List[str] = attr.ib(
            init=False,
            default=attr.Factory(
                lambda self: sorted(
                    set(glob(path.join(self.root_dir, '**/**'), recursive=True))
                ),
                takes_self=True,
            ),
        )

        def __iter__(self) -> t.Iterator[Path]:
            """Iterate alphabetically over files (not dirs) inside the Project.

            Iterate alphabetically over the absolute file paths (not
            directories) that reside (recursively) inside the Project (root
            folder).

            Returns:
                t.Iterator[str]: [description]

            Yields:
                Iterator[t.Iterator[str]]: [description]
            """
            for file_path in Path(self.root_dir).rglob('*'):
                if path.isfile(file_path) and '__pycache__' not in str(file_path):
                    yield file_path

        def relative_file_paths(self) -> t.Iterator[Path]:
            """Iterate alphabetically over relative file paths of the Project.

            Iterate alphabetically over the relative file paths (not
            directories) that reside (recursively) inside the Project (root
            folder).

            Returns:
                t.Iterator[str]: [description]
            """
            for file_path in iter(self):
                relative_path = file_path.relative_to(Path(self.root_dir))
                if (
                    str(relative_path) != str(Path('.git'))
                    and not str(relative_path).startswith(str(Path('.git/')))
                ) or str(relative_path).startswith(str(Path('.github/'))):
                    # assert not str(relative_path).startswith(
                    #     "cookie-py.log"
                    # ), f"Found {relative_path} in {self.root_dir}."
                    yield relative_path

    def _ret(root_dir: t.Union[str, Path]) -> RelativePathsGenerator:
        return ProjectFiles(root_dir)

    return _ret


@pytest.fixture
def get_expected_generated_files(
    distro_loc: Path,
    project_files: t.Callable[[t.Union[str, Path]], RelativePathsGenerator],
) -> t.Callable[[ConfigInterfaceGeneric[ConfigProtocol]], t.Set[Path]]:
    """Derive Expected Files, Pre-Generation, for sanity checks Post-Generation.

    Callable accepting a Config, User's Yaml or Default Json, and returning the
    Files which should be created, if the Generator is called with that Config.

    Useful for End-to-End Tests, with flow:
     - Configure -> Generate -> Project -> Assert

    Example Testing Scenario:
     - 1. Declare what to Generate in a Config (User's yaml or Default json) file
     - 2. Dynamically compute the Expected Files, given the Config
     - 2. Call Generator: ie using the CLI, or the cookiecutter_python Python API
     - 3. Assert Generated Files (runtime) are the Expected Files (pre-Generation)

    Callable that, given Configuration info, derives what files should be
    expected to be Generated (ie rendered from Templates), given the
    Configuration, either User's Yaml or Default (json) file, intended to be
    given as Input (ie values for Template Variables) to the Generator.

    Checks the Config argument at runtime, to Automatically derive the Expected
    Files, by consulting with the Template (jinja) Project contents.

    Template Project: src/cookiecutter_python/{{ cookiecutter.project_slug }}/

    Args:
        config (t.Mapping[str, t.Any]): Configuration, either User's Yaml or
            Default (json) file, intended to be given as Input (ie values for
            Template Variables) to the Generator.
    """
    from pathlib import Path

    from cookiecutter_python.hooks.post_gen_project import (
        delete_files as proj_type_2_files_to_remove,
    )

    def _get_expected_generated_files(config):
        expected_project_type = config.data['project_type']

        pkg_name: str = config.data['pkg_name']
        assert (
            'docs_builder' in config.data
        ), f"Missing 'docs_builder' in {config.data}. Probaly, user config Yaml supplied is missing templated values, required by cookiecutter.json."
        user_docs_builder_id: str = config.data['docs_builder']

        expected_gen_files: t.Set[Path] = set()
        expected_to_find: t.Set = set()

        ## DERIVE the EXPECTED files to be removed, varying across 'Project Type'
        # we leverage the same production logic
        ii = [
            x
            for x in proj_type_2_files_to_remove[expected_project_type](
                type(
                    'PostGenRequestLike',
                    (),
                    {
                        'module_name': pkg_name,
                    },
                )
            )
        ]
        SEP = '/'
        files_to_remove: t.Set[str] = {SEP.join(i) for i in ii}

        ## DERIVE expected files inside 'docs' gen dir
        from cookiecutter_python.backend import get_docs_gen_internal_config

        # Find where each Docs Builder 'stores' its Template Files (ie source docs)
        _doc_builder_id_2_template_docs_dir_name: t.Dict[str, str] = (
            get_docs_gen_internal_config()
        )
        builder_docs_folder_name: str = _doc_builder_id_2_template_docs_dir_name[
            user_docs_builder_id
        ]
        source_docs_template_content_dir: Path = (
            distro_loc / r'{{ cookiecutter.project_slug }}' / builder_docs_folder_name
        )

        # those docs template dir, are expected to be found under 'docs' folder
        for file_path in iter(
            (x for x in source_docs_template_content_dir.rglob('*') if x.is_file())
        ):
            assert isinstance(file_path, Path)
            # assert file_path is relative to docs_template_dir
            rp = file_path.relative_to(source_docs_template_content_dir)
            assert file_path.relative_to(source_docs_template_content_dir)
            expected_to_find.add(Path('docs') / rp)

        # Now expected_to_find, should be populated with files names/paths that
        # should be expected to be rendered for the requested docs builder in the config
        # ie if mkdocs -> {{ cookiecutter.project_slug }}/docs-mkdocs/**
        # are Put into our Expectations value 'expected_to_find'

        # pre-emptively any .pyc file from expected_to_find, since a bug was reported
        # where the .pyc file was not removed
        expected_to_find = {
            x
            for x in expected_to_find
            if not str(x).endswith('.pyc') and not str(x).endswith('__pycache__')
        }

        assert not any(
            [str(x).endswith('.pyc') for x in expected_to_find]
        ), f"Sanity check fail: {expected_to_find}"

        ## DERIVE the EXPECTED root-level files for post removal, based on docs-builer type
        # we leverage the same production mapping of builder_id to files
        from cookiecutter_python.hooks.post_gen_project import builder_id_2_files

        for docs_builder_id, builder_files in builder_id_2_files.items():
            if docs_builder_id != config.data['docs_builder']:
                assert all(
                    [isinstance(x, str) for x in builder_files]
                ), f"Temporary Requirement of Test Code: builder_files must be a list of strings, not {builder_files}"
                files_to_remove.update(builder_files)
        assert all(
            [isinstance(x, str) for x in files_to_remove]
        ), f"Temporary Requirement of Test Code: files_to_remove must be a list of strings, not {files_to_remove}"

        ## Remove all Template Docs files from Expectations
        for (
            docs_builder_id,
            builder_docs_folder_name,
        ) in _doc_builder_id_2_template_docs_dir_name.items():
            for file_path in iter(
                (
                    x
                    for x in Path(
                        distro_loc
                        / r'{{ cookiecutter.project_slug }}'
                        / builder_docs_folder_name
                    ).rglob('*')
                    if x.is_file()
                )
            ):
                # assert only Path instances are in the loop
                assert isinstance(
                    file_path, Path
                ), f"Temporary Requirement of Test Code: file_path must be a Path instance, not {file_path}"

                # see that file_path is relative to the distro_loc / r'{{ cookiecutter.project_slug }}'
                assert (
                    file_path.relative_to(
                        distro_loc / r'{{ cookiecutter.project_slug }}'
                    ).parts[0]
                    == builder_docs_folder_name
                ), f"Sanity check fail: {file_path.relative_to(distro_loc / r'{{ cookiecutter.project_slug }}')}, {file_path.relative_to(distro_loc / r'{{ cookiecutter.project_slug }}').parts[0]}"

                files_to_remove.add(
                    str(file_path.relative_to(distro_loc / r'{{ cookiecutter.project_slug }}'))
                )

        assert all(
            [isinstance(x, str) for x in files_to_remove]
        ), f"Temporary Requirement of Test Code: files_to_remove must be a list of strings, not {files_to_remove}"

        # FIND WHAT is actually in GEN ProJ DIR
        all_template_files = project_files(distro_loc / r'{{ cookiecutter.project_slug }}')

        assert all(
            [isinstance(x, str) for x in files_to_remove]
        ), f"Temporary Requirement of Test Code: files_to_remove must be a list of strings, not {files_to_remove}"

        sanity_check_files = [  # build up proper info for the expected files
            Path(str(x).replace(r'{{ cookiecutter.pkg_name }}', pkg_name))
            for x in all_template_files.relative_file_paths()
        ]

        # some adhoc sanity checks
        assert str(Path('.github/workflows/test.yaml')) in set(
            [str(_) for _ in sanity_check_files]
        )
        assert all(
            [
                str(Path(x)) in set([str(_) for _ in sanity_check_files])
                for x in (
                    '.github/workflows/test.yaml',
                    'pyproject.toml',
                    f"src/{pkg_name}/__init__.py",
                    'tests/conftest.py',
                    'mkdocs.yml',
                )
            ]
        )
        assert (
            len(set([type(x) for x in expected_to_find])) == 1
        ), f"Sanity check fail: {expected_to_find}"
        assert (
            len(set([type(x) for x in files_to_remove])) == 1
        ), f"Sanity check fail: {files_to_remove}"

        # update based on derived expected post deletions to happen
        expected_gen_files = set(
            [
                x
                for x in [i for i in all_template_files.relative_file_paths()]
                if x not in set([Path(_) for _ in files_to_remove])
            ]
        )
        # Regression Test
        # assert no .pyc files apear as has reported on sdist installation
        assert not any(
            [str(x).endswith('.pyc') for x in expected_gen_files]
        ), f"Sanity check fail: {expected_gen_files}"

        assert (
            len(set([type(x) for x in expected_gen_files])) == 1
        ), f"Sanity check fail: {expected_gen_files}"

        # update based on derived post renamings to happen
        so_far: int = len(expected_gen_files)

        expected_gen_files.update(expected_to_find)

        assert not any(
            [str(x).endswith('.pyc') for x in expected_gen_files]
        ), f"pyc files found: {[str(x.name) for x in expected_gen_files if str(x).endswith('.pyc')]}"

        assert (
            len(set([type(x) for x in expected_gen_files])) == 1
        ), f"Sanity check fail: {expected_gen_files}"
        # sanity check on posix path
        assert isinstance(
            list(expected_gen_files)[0], Path
        ), f"Sanity check fail: {expected_gen_files}"

        assert len(expected_gen_files) == so_far + len(
            expected_to_find
        ), "Our logic for deriving the expected files is wrong."

        ## Inject Values in TEMPLATE placeholders ##
        # TODO: use comprenhesoin once stable, and then ease maintainace, with some automation
        res = []
        for x in expected_gen_files:
            parts = x.parts
            assert type(parts) == tuple, f"Sanity check fail: {parts}"
            assert len(parts) > 0, f"Sanity check fail: {parts}"
            b = SEP.join(parts)
            b = b.replace(r'{{ cookiecutter.pkg_name }}', pkg_name).replace(
                r'{{ cookiecutter.project_slug }}', config.data['project_slug']
            )

            expected_file_parts = b.split(SEP)
            assert len(expected_file_parts) > 0, f"Sanity check fail: {expected_file_parts}"
            assert expected_file_parts[-1] != '', f"Sanity check fail: {expected_file_parts}"
            assert len(expected_file_parts) == len(
                parts
            ), f"Sanity check fail: {expected_file_parts}, {parts}"
            assert len(expected_file_parts) == len(
                x.parts
            ), f"Sanity check fail: {expected_file_parts}, {x.parts}"
            assert isinstance(
                expected_file_parts, list
            ), f"Sanity check fail: {expected_file_parts}"
            c: Path = Path(*expected_file_parts)
            res.append(c)

        assert len(set([type(x) for x in res])) == 1, f"Sanity check fail: {res}"

        # Filter again through predicted for removale since some of them already inject their value for distro name
        return iter(set([x for x in res if x not in set([Path(_) for _ in files_to_remove])]))

    return _get_expected_generated_files


# ASSERT Fixtures


@pytest.fixture
def assert_commit_author_is_expected_author(assert_initialized_git):
    def _assert_commit_author_is_expected_author(project_dir: str, expected_commit):
        repo = assert_initialized_git(project_dir)
        latest_commit = repo.commit('HEAD')
        assert latest_commit.type == 'commit'
        assert str(latest_commit.message).startswith(expected_commit.message)
        assert str(latest_commit.author.name) == expected_commit.author
        assert str(latest_commit.author.email) == expected_commit.email

    return _assert_commit_author_is_expected_author


@pytest.fixture
def assert_initialized_git():
    from git import Repo
    from git.exc import InvalidGitRepositoryError

    def _assert_initialized_git(folder: str):
        try:
            repo = Repo(folder)
            return repo
        except InvalidGitRepositoryError as error:
            raise error

    return _assert_initialized_git


@pytest.fixture
def assert_files_committed_if_flag_is_on(
    assert_initialized_git,
    assert_commit_author_is_expected_author,
    get_expected_generated_files,
    project_files,
):
    from os import path
    from pathlib import Path

    from git.exc import InvalidGitRepositoryError

    def is_root_file_committed(rel_path, tree):
        return str(rel_path) in tree

    def is_nested_file_committed(rel_path, tree):
        parent_tree = tree[str(rel_path.parent).replace('\\', '/')]
        blobs_set = {Path(blob.path) for blob in parent_tree}
        return rel_path in blobs_set

    def _assert_files_commited(folder, config):
        print("\n HERE")
        try:
            repo = assert_initialized_git(folder)

            head = repo.active_branch.commit
            assert head
            tree = repo.heads.master.commit.tree

            def file_commited(relative_path: Path):
                assert str(relative_path)[-1] != '/'
                splitted = path.split(relative_path)

                if splitted[0] == '':
                    return is_root_file_committed(relative_path, tree)
                else:
                    return is_nested_file_committed(relative_path, tree)

            # Sanity checks
            assert len(tree.trees) > 0  # trees are subdirectories
            assert len(tree.blobs) > 0  # blobs are files
            assert len(tree.blobs) + len(tree.trees) == len(tree)
            assert tree['src'] == tree / 'src'  # access by index & by sub-path

            # logic tests
            runtime_generated_files = set(project_files(folder).relative_file_paths())

            # A bug appeared that the runtime generated files include the logs file of cookiecutter_python distro
            for f in runtime_generated_files:
                # verify there is not top levevel distro log file generated/reported
                assert not str(f).endswith('cookie-py.log'), f"Documented Bug: {f}"
            assert 0, "Print Runtime Generated Files: " + '\n'.join(
                [str(f) for f in runtime_generated_files]
            )
            # below we assert that all the expected files have been commited:
            # 1st assert all generated runtime project files have been commited
            for f in sorted(runtime_generated_files):
                assert file_commited(f)
            # 2nd assert the generated files exactly match the expected ones
            expected_generated_files = get_expected_generated_files(config)
            assert set(runtime_generated_files) == set(expected_generated_files)

            assert_commit_author_is_expected_author(
                folder,
                type(
                    'Commit',
                    (),
                    {
                        'message': 'Template applied from',
                        'author': config.data['author'],
                        'email': config.data['author_email'],
                    },
                ),
            )
        except InvalidGitRepositoryError:
            return

    return _assert_files_commited
