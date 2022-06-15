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
    'config_file',
    [
        '.github/biskotaki.yaml',
        # pytest.param(None, marks=pytest.mark.xfail(
        #     reason="We do not support yet, the 'check-pypi feature, if --config-file is NOT supplied.")),
        None,
        'without-interpreters'
    ],
ids=['biskotaki', 'None', 'without-interpreters'])
def test_cli_offline(config_file, mock_check_pypi, user_config, cli_invoker_params,
    assert_files_committed_if_flag_is_on,
    isolated_cli_runner,
    tmpdir,
):
    import os
    from cookiecutter_python.cli import main as cli_main

    mock_check_pypi(exists_on_pypi=False)
    config = user_config[config_file]

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
            '--config-file': config.config_file,
            '--output-dir': tmpdir,
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
        os.path.abspath(os.path.join(tmpdir, config.pypi_name)), config=config
    )
    # s1 = (
    #     f"Name '{config.pypi_name}' IS available on pypi.org!\n"
    #     "You will be able to publish your Python Package on pypi as it is!"
    # )
    # assert s1 in result.stdout

