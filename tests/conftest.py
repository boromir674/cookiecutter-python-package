import os
import typing as t

import attr
import pytest

my_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def production_template() -> str:
    import cookiecutter_python

    return os.path.dirname(cookiecutter_python.__file__)


@pytest.fixture
def load_json() -> t.Callable[[str], t.Dict]:
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
def test_context(load_json, test_context_file) -> t.Dict:
    return load_json(test_context_file)


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


@pytest.fixture
def generate_project() -> t.Callable[[ProjectGenerationRequestData], str]:
    """Generator backend used by the production Generator CLI."""
    from cookiecutter_python.backend.generator import generator as cookiecutter

    def _generate_project(generate_request: ProjectGenerationRequestData) -> str:
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
def project_dir(
    generate_project,
    project_files,
    get_expected_generated_files,
    test_project_generation_request,
    production_templated_project,
):
    """Generate a Fresh new Project using the production cookiecutter template and
    the tests/data/test_cookiecutter.json file as default dict."""
    proj_dir: str = generate_project(test_project_generation_request)
    # runtime_files = os.listdir(proj_dir)
    # runtime_files = glob(f'{proj_dir}/*/**')
    # # we add '.git' since the project we generate for testing purposes
    # # uses a 'test_context' that instructs cookiecutter to initialiaze a git
    # # repo (see post_gen_project.py hook)
    # expected_files = os.listdir(production_templated_project) + ['.git']
    # expected_files = expected_generated_files()
    # assert set(expected_files) == set(runtime_files)
    # assert len(expected_files) == len(runtime_files)
    # assert all(['tox.ini' in x for x in (expected_files, runtime_files)])

    # p = os.path.abspath(os.path.join(proj_dir, '.github', 'workflows', 'test.yaml'))
    # with open(p, 'r') as f:
    #     contents = f.read()
    # import re

    # ver = r'"3\.(?:[6789]|10|11)"'
    # # assert build matrix definition includes one or more python interpreters
    # assert re.search(  # python-version: ["3.6", "3.7", "3.8", "3.9", "3.10"]
    #     fr'python-version:\s*\[\s*{ver}(?:(?:\s*,\s*{ver})*)\s*\]', contents
    # )

    # # assert that python interpreters are the expected ones given that we
    # # invoke the 'generate_project' function:
    # # no user yaml config & enabled the default_dict Flag!
    # b = ', '.join(
    #     (
    #         f'"{int_ver}"'
    #         for int_ver in test_project_generation_request.extra_context['interpreters'][
    #             'supported-interpreters'
    #         ]
    #     )
    # )
    # assert f"python-version: [{b}]" in contents
    # assert 'python-version: ["3.7", "3.8", "3.9"]' in contents

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
        project_type: t.Optional[t.Literal['module', 'module+cli', 'pytest-plugin']] = attr.ib(
            default='module'
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
def mock_check_pypi(get_object):
    """Mock and return the `check_pypi` function (with side effects).

    Returns a callable than when called mocks the check_pypi function so that
    there is no actual network (ie no connections though the internet) access.

    Calling the returned object yields side effects in order to facilitate
    mocking.

    You can then either directly use the returned `check_pypi` function
    (which shall trigger the mocked behaviour), or test your own code, which
    shall trigger the mocked behaviour if it depends on (the "original")
    `check_pypi`.

    Args:
        exists_on_pypi (t.Optional[bool]): whether to emulate that the package
            exists on pypi, or not. Defaults to False (package does NOT exist
            on pypi).

    Returns:
        t.Callable: a reference to the `check_pypi` function
    """

    class FutureMock:
        def __init__(self, exists_on_pypi: bool = False):
            self.result = lambda: type(
                'HttpResponseMock', (), {'status_code': 200 if exists_on_pypi else 404}
            )

    def get_check_pypi_with_mocked_futures_session(
        exists_on_pypi: bool = False,
    ) -> t.Callable[..., t.Any]:  # todo specify
        """Mocks FuturesSession and returns the 'check_pypi' object."""

        return get_object(
            'check_pypi',
            'cookiecutter_python.backend.check_pypi',
            overrides={
                "FuturesSession": lambda: type(
                    'MockFuturesSession',
                    (),
                    {'get': lambda self, url: FutureMock(exists_on_pypi)},
                )
            },
        )

    return get_check_pypi_with_mocked_futures_session


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
            # cwd=project_directory,
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


# Generic fixtures
@pytest.fixture
def path_builder() -> t.Callable[..., t.Callable[[str], str]]:
    """Convert relative to absolute file paths, given their root directory.

    Supply a root directory and get a callback that conveniently converts
    relative file paths to absolute, at runtime. The root directory can be a
    string, a Path or multiple strings/path (that os.join can 'join' together)

    Creates a callback that receives a single relative path (string) as input
    and returns an absolute file path (string).
    """
    from os import path

    def get_path_builder(root_path) -> t.Callable[[str], str]:
        def get_file(*relative_file_path: str) -> str:
            return path.join(
                root_path,
                *[
                    x
                    for l in [path_string.split('/') for path_string in relative_file_path]
                    for x in l
                ],
            )

        return get_file

    return get_path_builder


# Python Package Generator specific fixtures/fixtures


@pytest.fixture
def load_yaml():
    """Parse a yaml file using the 'production' Yaml Parser.

    Returns:
        t.Callable[[str], t.Mapping]: a callback that parses yaml files
    """
    from cookiecutter_python.backend.load_config import load_yaml

    return load_yaml


DataLoader = t.Callable[[str], t.MutableMapping]


@pytest.fixture
def user_config(load_yaml, load_json, path_builder, production_templated_project):
    from os import path

    config_files = {
        'biskotaki': '.github/biskotaki.yaml',
        'without-interpreters': 'tests/data/biskotaki-without-interpreters.yaml',
    }
    get_file = path_builder(path.abspath(path.join(my_dir, '..')))

    @attr.s(auto_attribs=True, slots=True)
    class ConfigData:
        path: t.Union[str, None]

        _data_file_path: t.Union[str, None] = attr.ib(init=False, default=None)
        _config_file_arg: t.Optional[str] = attr.ib(init=False, default=None)
        _loader: DataLoader = attr.ib(init=False)
        data: t.Mapping = attr.ib(init=False)

        def __attrs_post_init__(self):
            self._data_file_path, self._config_file_arg, self._loader = self._build_data(
                self.path
            )
            self.data = self._loader(self._data_file_path)

        @staticmethod
        def _build_data(
            file_path: t.Union[str, None]
        ) -> t.Tuple[str, t.Union[str, None], DataLoader]:
            if file_path is not None:
                data_file = get_file(config_files.get(file_path, file_path))
                return (
                    data_file,
                    data_file,
                    ConfigData.load_yaml(load_yaml),
                )
            return (
                path.abspath(
                    path.join(production_templated_project, '..', 'cookiecutter.json')
                ),
                None,
                ConfigData.load_json(load_json),
            )

        @staticmethod
        def load_json(loader: DataLoader):
            def _load_json(json_file: str):
                data = loader(json_file)
                data['project_slug'] = data['project_name'].lower().replace(' ', '-')
                data['author'] = data['full_name']
                data['pkg_name'] = data['project_name'].lower().replace(' ', '_')
                data['initialize_git_repo'] = {'yes': True}.get(
                    data['initialize_git_repo'][0], False
                )
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
            return self.data['project_slug']

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
def project_files():
    """Files of a generated Project, as iterable of file paths (excluding dirs)."""
    from glob import glob
    from os import path
    from pathlib import Path

    import attr

    @attr.s(auto_attribs=True, slots=True, frozen=True)
    class ProjectFiles:
        root_dir: str
        _glob: t.List[str] = attr.ib(
            init=False,
            default=attr.Factory(
                lambda self: sorted(
                    set(glob(path.join(self.root_dir, '**/**'), recursive=True))
                ),
                takes_self=True,
            ),
        )

        def __iter__(self) -> t.Iterator[str]:
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
                    yield str(file_path)

        def relative_file_paths(self) -> t.Iterator[str]:
            """Iterate alphabetically over relative file paths of the Project.

            Iterate alphabetically over the relative file paths (not
            directories) that reside (recursively) inside the Project (root
            folder).

            Returns:
                t.Iterator[str]: [description]
            """
            for file_path in iter(self):
                relative_path = str(path.relpath(file_path, start=self.root_dir))
                if relative_path != '.git' and not relative_path.startswith('.git/'):
                    yield relative_path

    return ProjectFiles


@pytest.fixture
def get_expected_generated_files(production_templated_project, project_files):
    from os import path

    from cookiecutter_python.hooks.post_gen_project import delete_files

    def _get_expected_generated_files(folder, config):
        expected_project_type = config.data['project_type']
        request = type(
            'PostGenRequestLike',
            (),
            {
                'project_dir': folder,
                'project_type': expected_project_type,
                'module_name': config.data['pkg_name'],
            },
        )
        files_to_remove = [path.join(*x) for x in delete_files[expected_project_type](request)]

        all_template_files = project_files(production_templated_project)
        expected_files = [
            x.replace(r'{{ cookiecutter.pkg_name }}', config.data['pkg_name'])
            for x in all_template_files.relative_file_paths()
        ]
        print('\nEXPECTED FILES:\n', '\n'.join(expected_files))
        # some adhoc sanity checks
        assert all(
            [
                x in set(expected_files)
                for x in (
                    '.bettercodehub.yml',
                    '.github/workflows/test.yaml',
                    'pyproject.toml',
                )
            ]
        )
        return iter(x for x in expected_files if x not in set(files_to_remove))

    return _get_expected_generated_files


@pytest.fixture
def assert_files_committed_if_flag_is_on(assert_files_commited):
    def _assert_files_committed_if_flag_is_on(project_dir, config):
        assert_files_commited(project_dir, config)

    return _assert_files_committed_if_flag_is_on


@pytest.fixture
def assert_files_commited(
    assert_initialized_git,
    assert_commit_author_is_expected_author,
    get_expected_generated_files,
    project_files,
):
    from os import path

    from git.exc import InvalidGitRepositoryError

    d = {
        1: lambda rel_path, tree: rel_path in tree,
        0: lambda rel_path, tree: rel_path in tree[path.split(rel_path)[0]],
    }

    def _assert_files_commited(folder, config):
        try:
            repo = assert_initialized_git(folder)

            head = repo.active_branch.commit
            assert head
            tree = repo.heads.master.commit.tree

            def file_commited(relative_path: str):
                splitted = path.split(relative_path)

                return d[splitted[0] == '' or splitted[1] == ''](
                    relative_path,
                    tree,
                )

            # Sanity checks
            assert len(tree.trees) > 0  # trees are subdirectories
            assert len(tree.blobs) > 0  # blobs are files
            assert len(tree.blobs) + len(tree.trees) == len(tree)
            assert tree['src'] == tree / 'src'  # access by index & by sub-path

            # logic tests
            runtime_generated_files = set(project_files(folder).relative_file_paths())
            # below we assert that all the expected files have been
            # commited:
            # 1st assert all generated runtime project files have been commited
            for f in runtime_generated_files:
                assert file_commited(f)
            # 2nd assert the generated files exactly match the expected one
            expected_generated_files = get_expected_generated_files(folder, config)
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
