import pytest


@pytest.fixture
def main_command():
    from cookiecutter_python.cli import main

    return main


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli(main_command, generate_python_args, isolated_cli_runner):
    args, kwargs = generate_python_args(output_dir='gen')
    assert type(kwargs) == dict
    assert type(args) == list
    result = isolated_cli_runner.invoke(
        main_command,
        args=args,
        input=None,
        env=None,
        catch_exceptions=False,
        color=False,
        **kwargs,
    )
    assert result.exit_code == 0


@pytest.fixture
def mock_check_pypi():
    def get_mock_check_pypi(answer: bool):
        return (
            type(
                'Future',
                (),
                {
                    'result': lambda: type(
                        'HttpResponse',
                        (),
                        {
                            'status_code': 200 if answer else 404,
                        },
                    )
                },
            ),
            'biskotaki',
        )

    return get_mock_check_pypi


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli_offline(get_object, mock_check_pypi, generate_python_args, isolated_cli_runner):
    args, kwargs = generate_python_args(output_dir='gen')
    cli_main = get_object('main', 'cookiecutter_python.cli')
    get_object(
        'generate',
        'cookiecutter_python.backend.main',
        overrides={"check_pypi": lambda: lambda x, y: mock_check_pypi(True)},
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
