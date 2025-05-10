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

    def _generate_project(
        generate_request: ProjectGenerationRequestDataProtocol,
    ) -> str:
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
    config_file: t.Union[str, None]


class ConfigInterfaceProtocol(t.Protocol):
    def __getitem__(self, file_path_str: t.Union[str, None]) -> ConfigProtocol:
        ...


@pytest.fixture
def user_config(distro_loc: Path) -> ConfigInterfaceProtocol:
    """Context Values Interface, derived either from User's YAML or Default JSON

    Args:
        distro_loc (Path): [description]

    Returns:
        [type]: [description]
    """
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

    def _load_context_yaml(file_path: PathLike) -> t.MutableMapping[str, t.Any]:
        return prod_load_yaml(file_path)['default_context']

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

        # _data_file_path: t.Union[str, Path, None] = attr.ib(init=False, default=None)
        _config_file_arg: t.Optional[Path] = attr.ib(init=False, default=None)
        _loader: DataLoader = attr.ib(init=False)
        _data: t.Mapping = attr.ib(init=False)

        config_files = {
            'biskotaki': '.github/biskotaki.yaml',
            'without-interpreters': 'tests/data/biskotaki-without-interpreters.yaml',
        }

        # When no Config File suppied values are derived from Ccookiecutter.json
        default_parameters = {
            'data_file': distro_loc / 'cookiecutter.json',
            'data_loader': lambda cls: lambda json_file_string_path: cls.transorm_json_data(
                _load_context_json(json_file_string_path)
            ),
        }

        def __attrs_post_init__(self):
            # called on user_config[config_file]

            _data_file_path = (
                ConfigData.default_parameters['data_file']
                if self.path is None
                else Path(my_dir) / '..' / ConfigData.config_files.get(self.path, self.path)
            )
            self._loader = (
                ConfigData.default_parameters['data_loader'](ConfigData)
                if self.path is None
                else lambda yaml_file_string_path: ConfigData.transorm_yaml_data(
                    _load_context_yaml(yaml_file_string_path)
                )
            )
            self._config_file_arg = _data_file_path if self.path is not None else None

            assert _data_file_path.exists()
            assert _data_file_path.is_file()

            self._data = self._loader(_data_file_path)

        @property
        def data(self) -> t.Mapping:
            """Get the computed 'default parameters' as standard python objects.

            Returns:
                t.Mapping: the 'default parameters' as standard python objects
            """
            return self._data

        @staticmethod
        def transorm_json_data(data: t.Dict[str, t.Any]):
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
            # CICD Pipeline Design old/new , stable/experimental
            data['cicd'] = data['cicd'][0]  # choice variable
            return data

        @staticmethod
        def transorm_yaml_data(data: t.Dict[str, t.Any]):
            data['initialize_git_repo'] = {'yes': True}.get(data['initialize_git_repo'], False)
            return data

        @property
        def project_slug(self) -> str:
            return self._data['project_slug']

        @property
        def config_file(self) -> t.Union[Path, None]:
            return self._config_file_arg

    # NOTE: this offers client code: user_config[config_file]
    # TODO: remove this unecessary adapter
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

    def relative_file_paths(self) -> t.Iterator[Path]:
        ...


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
) -> t.Callable[[ConfigInterfaceProtocol], t.Set[Path]]:
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
                type('PostGenRequestLike', (), {'module_name': pkg_name})
            )
        ]
        SEP = '/'
        files_to_remove: t.Set[str] = {SEP.join(i) for i in ii}

        # Augment the expected files for removal based on CI/CD option
        from cookiecutter_python.hooks.post_gen_project import CICD_DELETE

        files_to_remove.update(
            [os.path.join(*parts) for parts in CICD_DELETE[config.data.get('cicd', 'stable')]]
        )

        ## DERIVE expected files inside 'docs' gen dir

        def b(docs_builder_id):
            return (
                '{% if cookiecutter.docs_builder == "'
                + docs_builder_id
                + '" %}docs{% else %}PyGen_TO_DELETE{% endif %}'
            )

        # Find where each Docs Builder 'stores' its Template Files (ie source docs)
        selected_docs_template_dir: str = b(user_docs_builder_id)

        builder_docs_folder_name: str = selected_docs_template_dir
        source_docs_template_content_dir: Path = (
            distro_loc / r'{{ cookiecutter.project_slug }}' / selected_docs_template_dir
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
        from cookiecutter_python.hooks.post_gen_project import DOCS_FILES_EXTRA

        for docs_builder_id, builder_files in (
            (k, v) for k, v in DOCS_FILES_EXTRA.items() if k != config.data['docs_builder']
        ):
            assert all(
                [isinstance(x, str) for x in builder_files]
            ), f"Temporary Requirement of Test Code: builder_files must be a list of strings, not {builder_files}"
            files_to_remove.update(builder_files)
        assert all(
            [isinstance(x, str) for x in files_to_remove]
        ), f"Temporary Requirement of Test Code: files_to_remove must be a list of strings, not {files_to_remove}"

        ## Remove all Template Docs files from Expectations, because in the Template Project
        # 2 dedicated foldres are used to maintain mkdocs and spinx Docs (which get moved to ./docs in post hook)
        for (
            docs_builder_id,
            builder_docs_folder_name,
        ) in [
            (
                docs_builder_id,
                b(docs_builder_id),
            )
            for docs_builder_id in {'mkdocs', 'sphinx'}
        ]:  # TODO: centralize this
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
            assert type(parts) is tuple, f"Sanity check fail: {parts}"
            assert len(parts) > 0, f"Sanity check fail: {parts}"
            joined_parts: str = SEP.join(parts)
            joined_parts = joined_parts.replace(
                r'{{ cookiecutter.pkg_name }}', pkg_name
            ).replace(r'{{ cookiecutter.project_slug }}', config.data['project_slug'])

            expected_file_parts = joined_parts.split(SEP)
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
    try:
        from git import Repo
    except ImportError as error:
        # happens if git binary is not installed on host!
        print("Error: ", error)
        return lambda x: 'git binary not installed on host'

    from git.exc import InvalidGitRepositoryError

    def _assert_initialized_git(folder: str):
        try:
            repo = Repo(folder)
            return repo
        except InvalidGitRepositoryError as error:
            raise error

    return _assert_initialized_git


# TODO: retire or fix the logic of this "test"
@pytest.fixture
def assert_files_committed_if_flag_is_on(
    assert_initialized_git,
    # assert_commit_author_is_expected_author,
    # get_expected_generated_files,
    # project_files,
):
    from git.exc import InvalidGitRepositoryError

    def _assert_files_commited(folder, config):
        print("\n HERE")
        try:
            _repo = assert_initialized_git(folder)
        except InvalidGitRepositoryError:
            _repo = None
        return _repo

    return _assert_files_commited


# Proper SUBPROCESS wrapper


@pytest.fixture(scope="session")
def my_run_subprocess():
    import subprocess

    class CLIResult:
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

    def execute_command_in_subprocess(executable: str, *args, **kwargs):
        """Run command with python subprocess, given optional runtime arguments.

        Use kwargs to override subprocess flags, such as 'check'

        Flag 'check' defaults to True.
        """
        kwargs_dict = dict(
            capture_output=True,  # capture stdout and stderr separately
            # cwd=project_directory,
        )
        completed_process = subprocess.run(  # pylint: disable=W1510
            [executable] + list(args),
            **dict(dict(kwargs_dict, check=True, shell=False), **kwargs),
        )
        return CLIResult(completed_process)

    return execute_command_in_subprocess


@pytest.fixture
def dat(distro_loc: Path):
    import json
    from collections import OrderedDict

    my_dir = Path(__file__).resolve().parent

    # Read JSON data from 'tests/data/test_cookiecutter.json'
    # The JSON schema and values MUST reflect a valid internal state of the
    # Generator's Template Engine.
    # at the moment, we exclusively use cookiecutter (and jinja2) for templating
    # GIVEN data that reflect a state, which the Templating Engine is possible
    # to arrive at, when the Generator CLI is invoked.
    ### We want to skip running the templating engine, so we mock the state
    ### that the templating engine would have produced.
    engine_state: OrderedDict = json.loads(
        (my_dir / 'data' / 'test_cookiecutter.json').read_text(),
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
    state_keys = set(engine_state['cookiecutter'].keys())
    assert state_keys and state_keys.issubset(set(td_cookiecutter_json_data.keys()))

    # Templated Vars (cookiecutter) use in Context for Jinja Rendering

    return OrderedDict(td_cookiecutter_json_data, **engine_state['cookiecutter'])
