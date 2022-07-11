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


class CheckReadthedocsFeatureNotSupported(Exception):
    pass


reason = "We do not support yet, the 'check-pypi' feature, if --config-file is NOT supplied."


@pytest.mark.runner_setup(mix_stderr=False)
@pytest.mark.parametrize(
    'config_file, default_config',
    [
        ('.github/biskotaki.yaml', False),
        (None, True),
        ('without-interpreters', False),
        ('tests/data/pytest-fixture.yaml', False),
    ],
    ids=['biskotaki', 'None', 'without-interpreters', 'pytest-fixture'],
)
def test_cli_offline(
    config_file,
    default_config,
    mock_check,
    check_pypi_result,
    check_readthedocs_result,
    check_web_server_expected_result,
    user_config,
    cli_invoker_params,
    assert_files_committed_if_flag_is_on,
    assert_generated_expected_project_type,
    isolated_cli_runner,
    tmpdir,
):
    from os import path

    from cookiecutter_python.cli import main as cli_main

    config = user_config[config_file]

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
            '--config-file': config.config_file,
            '--output-dir': tmpdir,
            '--default-config': default_config,
        }
    )
    FOUND_ON_PYPI = False
    FOUND_ON_READTHEDOCS = False

    mock_check.config = config
    mock_check('pypi', FOUND_ON_PYPI)
    mock_check('readthedocs', FOUND_ON_READTHEDOCS)

    result = isolated_cli_runner.invoke(
        cli_main,
        args=args,
        input=None,
        env=None,
        catch_exceptions=False,
        color=False,
        **kwargs,
    )
    # print(result.stdout)
    assert result.exit_code == 0

    project_dir = path.abspath(path.join(tmpdir, config.project_slug))
    assert_files_committed_if_flag_is_on(project_dir, config=config)
    assert_generated_expected_project_type(project_dir, config)

    package_exists_on_pypi = check_pypi_result(result.stdout)
    assert package_exists_on_pypi == check_web_server_expected_result('pypi')(
        config, FOUND_ON_PYPI
    )

    package_exists_on_readthedocs = check_readthedocs_result(result.stdout)
    assert package_exists_on_readthedocs == check_web_server_expected_result('readthedocs')(
        config, FOUND_ON_READTHEDOCS
    )


@pytest.fixture
def assert_generated_expected_project_type(
    project_files,
    get_expected_generated_files,
):
    def _assert_generated_expected_project_type(project_dir: str, config):
        runtime_generated_files = set(project_files(project_dir).relative_file_paths())
        expected_gen_files = set(get_expected_generated_files(project_dir, config))
        assert runtime_generated_files == expected_gen_files

    return _assert_generated_expected_project_type


@pytest.fixture
def check_pypi_result(check_web_server) -> t.Callable[[str], t.Optional[bool]]:
    check_pypi_output = {
        'found': "You shall rename your Python Package first, if you choose to publish it on pypi!",
        'not-found': r"You will not need to rename your Python Package if you choose to publish it on pypi :\)",
    }

    def _check_pypi(cli_stdout: str) -> t.Optional[bool]:
        return check_web_server(cli_stdout, check_pypi_output)

    return _check_pypi


@pytest.fixture
def check_readthedocs_result(check_web_server) -> t.Callable[[str], t.Optional[bool]]:
    check_readthedocs_output = {
        'found': "You shall rename your Python Package first, if you choose to publish it on readthedocs!",
        'not-found': r"You will not need to rename your Python Package if you choose to publish it on readthedocs :\)",
    }

    def _check_readthedocs(cli_stdout: str) -> t.Optional[bool]:
        return check_web_server(cli_stdout, check_readthedocs_output)

    return _check_readthedocs


@pytest.fixture
def check_web_server() -> t.Callable[[str, t.Any], t.Optional[bool]]:
    import re

    def _check_web_server(cli_stdout: str, expected_messages) -> t.Optional[bool]:
        match = re.search(
            r'({found_message}|{not_found_message})'.format(
                found_message=expected_messages['found'],
                not_found_message=expected_messages['not-found'],
            ),
            cli_stdout,
        )
        if match:
            return match.group(1) == expected_messages['found']
        return None

    return _check_web_server


@pytest.fixture
def check_web_server_expected_result():
    webserver_2_templaet_variable = {
        'pypi': 'pkg_name',
        'readthedocs': 'readthedocs_project_slug',
    }

    def _build_get_check_web_server_expected_result(webserver: str):
        def _get_check_web_server_expected_result(config, mock_flag: bool):
            if (
                config.config_file is not None
                and webserver_2_templaet_variable[webserver] in config.data
            ):
                return mock_flag
            return None

        return _get_check_web_server_expected_result

    return _build_get_check_web_server_expected_result
