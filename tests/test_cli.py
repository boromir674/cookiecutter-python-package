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


import typing as t
class HttpResponseLike(t.Protocol):
    status_code: int
class FutureLike(t.Protocol):
    result: t.Callable[[], HttpResponseLike]

CheckPypiOutput = t.Tuple[FutureLike, str]

CheckPypi = t.Callable[[str, str], CheckPypiOutput]

@pytest.fixture
def get_check_pypi_mock() -> t.Callable[[t.Optional[bool]], CheckPypi]:
    def build_check_pypi_mock_output(emulated_success=True) -> FutureLike:
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
    def _get_check_pypi_mock(emulated_success: bool = True) -> t.Callable[..., CheckPypiOutput]:
        def check_pypi_mock(*args, **kwargs) -> CheckPypiOutput:
            return (
                build_check_pypi_mock_output(emulated_success=emulated_success),
                'biskotaki',
            )
        return check_pypi_mock

    return _get_check_pypi_mock


@pytest.fixture
def mock_check_pypi(get_check_pypi_mock, get_object):
    def get_generate_with_mocked_check_pypi(**overrides) -> t.Callable[..., t.Any]:  # todo specify
        """Mocks namespace and returns the 'generate' object."""
        return get_object('generate', 'cookiecutter_python.backend.main',
            overrides=dict(
                {"check_pypi": lambda: get_check_pypi_mock(emulated_success=True)}, **overrides))

    return get_generate_with_mocked_check_pypi

# @pytest.fixture
# def cli_main():
#     try:


# import sys
# @pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
# @pytest.mark.skipif(sys.version_info >= (3, 10), reason="requires python >= 3.6 or higher")
@pytest.mark.runner_setup(mix_stderr=False)
def test_cli_offline(mock_check_pypi, cli_invoker_params, isolated_cli_runner):
    from cookiecutter_python.cli import main as cli_main
    _generate = mock_check_pypi()

    args, kwargs = cli_invoker_params(optional_cli_args={
            '--no-input': True,
        })

    result = isolated_cli_runner.invoke(
        cli_main,
        args=args,
        input=None,
        env=None,
        catch_exceptions=False,
        color=False,
        **kwargs,
    )
    print('OUT:\n', result.stdout)
    assert result.exit_code == 0
