import typing as t

import pytest


@pytest.mark.parametrize(
    'config_file, expected_interpreters, spawned_cli',
    [
        ('.github/biskotaki.yaml', ['3.6', '3.7', '3.8', '3.9', '3.10'], False),
        (None, ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11'], False,),
        (
            'tests/data/biskotaki-without-interpreters.yaml',
            ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11'],
            True, 
        ),
    ],
)
def test_generate_with_mocked_network(
    config_file: str,
    expected_interpreters: t.Sequence[str],
    spawned_cli: bool,
    get_object,
    get_check_pypi_mock,
    assert_interpreters_array_in_build_matrix,
    tmpdir,
):
    generate = get_object(
        'generate',
        'cookiecutter_python.backend.main',
        overrides={"check_pypi": lambda: get_check_pypi_mock(emulated_success=True)},
    )
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
    
@pytest.fixture(params=[
    'src/my_new_project/cli.py',
    'src/my_new_project/__main__.py',
])
def expected_cli_related_file(request, project_dir) -> str:
    import os
    return os.path.join(project_dir, *list(request.param.split('/')))


def test_enabling_add_cli_templated_variable(expected_cli_related_file):
    import os
    assert os.path.isfile(expected_cli_related_file)



# ASSERT Fixtures


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


@pytest.fixture
def project_source_file():
    from os import path, listdir
    SRC_DIR_NAME = 'src'
    def build_get_file_path(project_dir: str) -> str:
        src_dir_files = listdir(path.join(project_dir, SRC_DIR_NAME))
        # sanity check that Generator produces only 1 python module/package
        [python_module] = src_dir_files
        def _get_file_path(file: str):
            return path.join(
                project_dir,
                SRC_DIR_NAME,
                python_module,
                *file.split('/')
            )
    return build_get_file_path


@pytest.fixture
def assert_scaffolded_without_cli(cli_related_file_name, project_source_file):
    from os import path
    def assert_project_generated_without_cli(project_dir: str):
        get_file: t.Callable[[str], str] = project_source_file(project_dir)
        # assert there are no cli related files
        assert not path.isfile(get_file(cli_related_file_name))
    return assert_project_generated_without_cli
