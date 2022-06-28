import typing as t

import pytest


@pytest.mark.parametrize(
    'config_file, expected_interpreters',
    [
        ('.github/biskotaki.yaml', ['3.6', '3.7', '3.8', '3.9', '3.10']),
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
    mock_check_pypi,
    assert_interpreters_array_in_build_matrix,
    assert_scaffolded_without_cli,
    tmpdir,
):
    from cookiecutter_python.backend.main import generate

    mock_check_pypi(exists_on_pypi=True)

    project_dir: str = generate(
        checkout=None,
        no_input=True,
        extra_context=None,
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
    import os

    def _assert_interpreters_array_in_build_matrix(
        project_dir: str,
        interpreters: t.Sequence[str],
    ) -> None:
        p = os.path.abspath(os.path.join(project_dir, '.github', 'workflows', 'test.yaml'))
        with open(p, 'r') as f:
            contents = f.read()

        b = ', '.join((f'"{int_ver}"' for int_ver in interpreters))
        assert f"python-version: [{b}]" in contents

    return _assert_interpreters_array_in_build_matrix


CLI_RELATED_FILES = {
    'cli.py',
    '__main__.py',
}


@pytest.fixture
def module_file(path_builder):

    from os import listdir, path

    SRC_DIR_NAME = 'src'

    def build_get_file_path(project_dir: str) -> t.Callable[[str], str]:
        get_file = path_builder(path.abspath(project_dir))
        src_dir_files = listdir(get_file(SRC_DIR_NAME))
        # sanity check that Generator produces only 1 python module/package
        [python_module] = src_dir_files

        def _get_file_path(*file_path):
            return get_file(SRC_DIR_NAME, python_module, *file_path)

        return _get_file_path

    return build_get_file_path


@pytest.fixture
def assert_scaffolded_without_cli(module_file) -> t.Callable[[str], None]:
    from os import path

    def assert_project_generated_without_cli(project_dir: str) -> None:
        get_file: t.Callable[[str], str] = module_file(project_dir)
        module_dir = get_file('')
        print('MODULE DIR:', module_dir)
        import os

        print(os.listdir(module_dir))
        # assert there are no cli related files
        assert all(not path.isfile(get_file(file_name)) for file_name in CLI_RELATED_FILES)

    return assert_project_generated_without_cli


@pytest.fixture(params=[x for x in CLI_RELATED_FILES])
def cli_related_file_name(request):
    return request.param


def test_enabling_add_cli_templated_variable(
    cli_related_file_name,
    module_file,
    project_dir,
):
    from os import path

    get_file = module_file(project_dir)
    assert path.isfile(get_file(cli_related_file_name))
