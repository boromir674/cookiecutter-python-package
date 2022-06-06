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
    get_object,
    get_check_pypi_mock,
    assert_interpreters_array_in_build_matrix,
    assert_scaffolded_without_cli,
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
    assert_scaffolded_without_cli(project_dir)


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
def assert_scaffolded_without_cli(
    cli_related_file_name, project_source_file
) -> t.Callable[[str], None]:
    from os import path

    def assert_project_generated_without_cli(project_dir: str) -> None:
        get_file: t.Callable[[str], str] = project_source_file(project_dir)
        # assert there are no cli related files
        assert not path.isfile(get_file(cli_related_file_name))

    return assert_project_generated_without_cli


@pytest.fixture(
    params=[
        'cli.py',
        '__main__.py',
    ]
)
def cli_related_file_name(request):
    return request.param


def test_enabling_add_cli_templated_variable(
    cli_related_file_name,
    project_source_file,
    project_dir,
):
    from os import path

    get_file = project_source_file(project_dir)
    assert path.isfile(get_file(cli_related_file_name))
