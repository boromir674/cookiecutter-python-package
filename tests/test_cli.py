import typing as t

import pytest


@pytest.mark.network_bound
@pytest.mark.runner_setup(mix_stderr=False)
def test_cli(cli_invoker_params, isolated_cli_runner):
    from cookiecutter_python.cli import main

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
        }
    )
    assert type(kwargs) == dict
    assert type(args) == list
    result = isolated_cli_runner.invoke(
        main,
        args=args,
        input=None,
        env=None,
        catch_exceptions=False,
        color=False,
        **kwargs,
    )
    assert result.exit_code == 0


class CheckPypiFeatureNotSupported(Exception):
    pass


reason = "We do not support yet, the 'check-pypi' feature, if --config-file is NOT supplied."


@pytest.mark.runner_setup(mix_stderr=False)
@pytest.mark.parametrize(
    'config_file, default_config',
    [
        ('.github/biskotaki.yaml', False),
        pytest.param(
            None,
            True,
            marks=pytest.mark.xfail(
                # exception=NotImplementedError,
                strict=True,
                reason=reason,
            ),
        ),
        ('without-interpreters', False),
        ('tests/data/pytest-fixture.yaml', False),
    ],
    ids=['biskotaki', 'None', 'without-interpreters', 'pytest-fixture'],
)
def test_cli_offline(
    config_file,
    default_config,
    check_pypi_result,
    mock_check_pypi,
    user_config,
    cli_invoker_params,
    assert_files_committed_if_flag_is_on,
    assert_generated_expected_project_type,
    isolated_cli_runner,
    tmpdir,
):
    from os import path

    from cookiecutter_python.cli import main as cli_main

    mock_check_pypi(exists_on_pypi=False)
    config = user_config[config_file]

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
            '--config-file': config.config_file,
            '--output-dir': tmpdir,
            '--default-config': default_config,
        }
    )
    result = isolated_cli_runner.invoke(
        cli_main,
        args=args,
        input=None,
        env=None,
        catch_exceptions=False,
        color=False,
        **kwargs,
    )
    assert result.exit_code == 0

    project_dir = path.abspath(path.join(tmpdir, config.project_slug))
    assert_files_committed_if_flag_is_on(project_dir, config=config)
    assert_generated_expected_project_type(project_dir, config)

    package_exists_on_pypi = check_pypi_result(result.stdout)
    if package_exists_on_pypi is None:
        raise CheckPypiFeatureNotSupported(reason)


@pytest.fixture
def assert_generated_expected_project_type(
    project_files,
    get_expected_generated_files,
):
    def _assert_generated_expected_project_type(project_dir: str, config):
        runtime_generated_files = set(project_files(project_dir).relative_file_paths())
        # expected_gen_files = set([str(file_path) for file_path in get_expected_generated_files(project_dir, config)])
        expected_gen_files = set(get_expected_generated_files(project_dir, config))
        assert runtime_generated_files == expected_gen_files

    return _assert_generated_expected_project_type


@pytest.fixture
def check_pypi_result() -> t.Callable[[str], t.Optional[bool]]:
    import re

    check_pypi_output = {
        'found': "You shall rename your Python Package before publishing to pypi!",
        'not-found': "You will be able to publish your Python Package on pypi as it is!",
    }
    check_pypi_reg_string = '({found_message}|{not_found_message})'.format(
        found_message=check_pypi_output['found'],
        not_found_message=check_pypi_output['not-found'],
    )

    def _check_pypi(cli_stdout: str) -> t.Optional[bool]:
        match = re.search(rf'{check_pypi_reg_string}\nFinished :\)', cli_stdout)
        if match:
            return match.group(1) in check_pypi_output.values()
        return None

    return _check_pypi
