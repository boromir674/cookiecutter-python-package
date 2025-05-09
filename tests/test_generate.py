import typing as t
from pathlib import Path

import pytest


@pytest.fixture
def assert_scaffolded_without_cli(module_file) -> t.Callable[[str], None]:
    from os import path

    def assert_project_generated_without_cli(project_dir: str) -> None:
        get_file: t.Callable[[str], str] = module_file(project_dir)
        assert all(not path.isfile(get_file(file_name)) for file_name in CLI_RELATED_FILES)

    return assert_project_generated_without_cli


# dynamic param 'marks' argument
tests_root: Path = Path(__file__).parent
RUNNING_FROM_LOCAL_CHECKOUT: bool = (tests_root.parent / '.github').exists()


@pytest.mark.parametrize(
    'config_file, expected_interpreters',
    [
        pytest.param(
            '.github/biskotaki.yaml',
            ['3.7', '3.8', '3.9', '3.10', '3.11'],
            marks=pytest.mark.skipif(
                not RUNNING_FROM_LOCAL_CHECKOUT,
                reason=f"'Running tests from within local checkout is required to test this feature. Current path: {tests_root}'",
            ),
        ),
        (None, ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11']),
        (
            'tests/data/biskotaki-without-interpreters.yaml',
            ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11'],
        ),
    ],
)
def test_supported_python_interpreters(
    config_file: str,
    expected_interpreters: t.Sequence[str],
    mock_check,
    user_config,
    assert_interpreters_array_in_build_matrix,
    assert_scaffolded_without_cli,
    tmpdir,
):
    from cookiecutter_python.backend.main import generate

    config = user_config[config_file]
    mock_check.config = config
    mock_check('pypi', True)
    mock_check('readthedocs', True)

    project_dir: str = generate(
        checkout=None,
        no_input=True,
        replay=False,
        overwrite=False,
        output_dir=tmpdir,
        config_file=config_file,
        default_config=False,
        password=None,
        directory=None,
        skip_if_file_exists=False,
    )

    assert_interpreters_array_in_build_matrix(project_dir, expected_interpreters)
    assert_scaffolded_without_cli(project_dir)


@pytest.fixture
def assert_interpreters_array_in_build_matrix() -> t.Callable[[str, t.Sequence[str]], None]:
    """Test that Job Matrix is generated correctly and stored as Workflow env var.

    Test proper generation of github workflow config yaml for lines such as:

    # FULL_MATRIX_STRATEGY: "{\"platform\": [\"ubuntu-latest\", \"macos-latest\", \"windows-latest\"], \"python-version\": [\"3.7\", \"3.8\", \"3.9\", \"3.10\", \"3.11\"]}"

    Returns:
        t.Callable[[str, t.Sequence[str]], None]: [description]
    """
    from pathlib import Path

    def _assert_interpreters_array_in_build_matrix(
        project_dir: str,
        interpreters: t.Sequence[str],
    ) -> None:
        p = Path(project_dir) / '.github' / 'workflows' / 'test.yaml'
        if not p.exists():
            p = Path(project_dir) / '.github' / 'workflows' / 'cicd.yml'
        assert p.exists()
        contents = p.read_text()
        b = ', '.join((fr'\"{int_ver}\"' for int_ver in interpreters))
        assert r'\"python-version\": ' in contents
        assert fr'\"python-version\": [{b}]' in contents, f'"{b}" not in "{contents}"'

    return _assert_interpreters_array_in_build_matrix


CLI_RELATED_FILES = (
    'cli.py',
    '__main__.py',
)
"""Files, only expected to be generated for cli type of Projects"""


@pytest.fixture
def module_file():
    from functools import reduce
    from os import listdir
    from pathlib import Path

    SRC_DIR_NAME: str = 'src'

    def build_get_file_path(project_dir: str) -> t.Callable[[str], str]:
        p: Path = Path(project_dir)
        src_dir_files = listdir(p / SRC_DIR_NAME)
        # sanity check that Generator produces only 1 python module/package
        assert len(src_dir_files) == 1
        python_module: str = src_dir_files[0]

        def _get_file_path(*file_path: t.Union[str, Path]):
            l1: t.List[t.Union[str, Path]] = [p, SRC_DIR_NAME, python_module]

            return reduce(lambda i, j: Path(i) / Path(j), l1 + [_ for _ in file_path])

        return _get_file_path

    return build_get_file_path


@pytest.fixture(params=[x for x in CLI_RELATED_FILES])
def cli_related_file_name(request):
    return request.param


def test_enabling_add_cli_templated_variable(
    cli_related_file_name,
    module_file,
    project_dir,
):
    """Test that 'module+cli' Project Type generates CLI-explicit files."""
    from os import path

    get_file = module_file(project_dir)
    assert path.exists(get_file(cli_related_file_name))
    assert path.isfile(get_file(cli_related_file_name))
