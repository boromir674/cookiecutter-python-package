import pytest


@pytest.fixture
def main_command():
    from cookiecutter_python.cli import main

    return main


@pytest.mark.network_bound
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


# @pytest.fixture
# def mock_check_pypi():
#     def get_mock_check_pypi(answer: bool):
#         return (
#             type(
#                 'Future',
#                 (),
#                 {
#                     'result': lambda: type(
#                         'HttpResponse',
#                         (),
#                         {
#                             'status_code': 200 if answer else 404,
#                         },
#                     )
#                 },
#             ),
#             'biskotaki',
#         )

#     return get_mock_check_pypi
import typing as t
class HttpResponseLike(t.Protocol):
    status_code: int
class FutureLike(t.Protocol):
    result: t.Callable[[], HttpResponseLike]

CheckPypi = t.Callable[[str, str], t.Tuple[FutureLike, str]]

@pytest.fixture
def get_check_pypi_mock():
    # def check_pypi_mock(config_file: str, default_config: str) -> t.Tuple[FutureLike, str]:

    def a(emulated_success=True):
        return type(
                'Future',
                (),
                {
                    'result': lambda: type(
                        'HttpResponse',
                        (),
                        {
                            'status_code': 200 if emulated_success else 404,
                        },
                    )
                },
            )
    def _get_check_pypi_mock(emulated_success: bool = True) -> FutureLike:
        def check_pypi_mock(*args, **kwargs) -> t.Tuple[FutureLike, str]:
            return (
                a(emulated_success=emulated_success),
                'biskotaki',
            )
        return check_pypi_mock

        # return (
        #     ,
        #     'biskotaki',
        # )

    return _get_check_pypi_mock


@pytest.fixture
def mock_check_pypi(
    get_object,
    get_check_pypi_mock,
):
    def get_generate_with_mocked_check_pypi(**overrides) -> t.Callable[..., t.Any]:  # todo specify
        """Mocks namespace and returns the 'generate' object."""
        return get_object('generate', 'cookiecutter_python.backend.main',
            overrides=dict(
                {"check_pypi": lambda: get_check_pypi_mock(emulated_success=True)}, **overrides))

    return get_generate_with_mocked_check_pypi


@pytest.mark.runner_setup(mix_stderr=False)
def test_cli_offline(
    get_object,
    mock_check_pypi, generate_python_args, isolated_cli_runner
):

    cli_main = get_object('main', 'cookiecutter_python.cli')
    _generate = mock_check_pypi()

    # cli_main = get_object('main', 'cookiecutter_python.cli', overrides=dict(
    #     {"get_request": lambda: mock_check_pypi}, **overrides
    # ),)
    # cli_main = get_object('main', 'cookiecutter_python.cli', overrides=dict(
    #     {"get_request": lambda: lambda: request_factory.pre()}, **overrides
    # ),)
    # args, kwargs = generate_python_args(output_dir='gen')
    args, kwargs = generate_python_args()
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
