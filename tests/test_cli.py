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
def test_cli_offline(mock_check_pypi, cli_invoker_params, isolated_cli_runner):
    from cookiecutter_python.cli import main as cli_main

    mock_check_pypi()

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
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
    s1 = (
        "Name 'biskotaki' IS available on pypi.org!\n"
        "You will be able to publish your Python Package on pypi as it is!"
    )
    assert s1 in result.stdout
