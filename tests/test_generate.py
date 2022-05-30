import typing as t
import pytest


@pytest.mark.parametrize('config_file, expected_interpreters', [
    ('.github/biskotaki.yaml', ['3.6', '3.7', '3.8', '3.9', '3.10']),
    (None, ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11']),
    (
        'tests/data/biskotaki-without-interpreters.yaml',
        ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11']
    ),
])
def test_generate_with_mocked_network(
    config_file: str,
    expected_interpreters: t.Sequence[str],
    get_object,
    get_check_pypi_mock,
    assert_interpreters_array_in_build_matrix,
    tmpdir,
):
    generate = get_object('generate', 'cookiecutter_python.backend.main',
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

    assert_interpreters_array_in_build_matrix(
        project_dir, expected_interpreters
    )



# ASSERT Fictures


@pytest.fixture
def assert_interpreters_array_in_build_matrix() -> t.Callable[[str, t.Sequence[str]], None]:
    import os
    def _assert_interpreters_array_in_build_matrix(
        project_dir: str,
        interpreters: t.Sequence[str],
    ) -> None:
        p = os.path.abspath(os.path.join(project_dir, '.github', 'workflows',
            'test.yaml') )
        with open(p, 'r') as f:
            contents = f.read()
        
        b = ', '.join((f'"{int_ver}"' for int_ver in interpreters))
        assert f"python-version: [{b}]" in contents
    return _assert_interpreters_array_in_build_matrix