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
                reason="We do not support yet, the 'check-pypi' feature, if --config-file is NOT supplied.",
            ),
        ),
        ('without-interpreters', False),
    ],
    ids=['biskotaki', 'None', 'without-interpreters'],
)
def test_cli_offline(
    config_file,
    default_config,
    check_pypi_result,
    mock_check_pypi,
    user_config,
    cli_invoker_params,
    assert_files_committed_if_flag_is_on,
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
    assert_files_committed_if_flag_is_on(
        path.abspath(path.join(tmpdir, config.pypi_name)), config=config
    )
    package_exists_on_pypi = check_pypi_result(result.stdout)
    if package_exists_on_pypi is None:
        raise NotImplementedError


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
            print('CHECK PYPI MATCHED!:\n', match.group(1))
            return match.group(1) in check_pypi_output.values()
        return None

    return _check_pypi
