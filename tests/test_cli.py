import logging
import typing as t
from pathlib import Path

import pytest


logger = logging.getLogger(__name__)


@pytest.mark.network_bound
@pytest.mark.runner_setup(mix_stderr=False)
def test_cli(cli_invoker_params, isolated_cli_runner):
    from cookiecutter_python.cli import main

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
        }
    )
    assert isinstance(kwargs, dict)
    assert isinstance(args, list)
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


# dynamic param 'marks' argument
tests_root: Path = Path(__file__).parent

# RUNNING_FROM_LOCAL_CHECKOUT: bool = (tests_root.parent / 'src' / 'cookiecutter_python' / '__init__.py').exists()
RUNNING_FROM_LOCAL_CHECKOUT: bool = (tests_root.parent / '.github').exists()


@pytest.mark.runner_setup(mix_stderr=False)
@pytest.mark.parametrize(
    'config_file, default_config',
    [
        # Test Case 1: with CI BISKOTAKI User Config
        pytest.param(
            '.github/biskotaki.yaml',
            False,
            marks=pytest.mark.skipif(
                not RUNNING_FROM_LOCAL_CHECKOUT,
                reason=f"'Running tests from within local checkout is required to test this feature. Current path: {tests_root}'",
            ),
        ),
        # Test Case 2: No User Config + enable ~/.cookiecutterrc
        (None, True),
        # Test Case 3: biskotaki-without-interpreters.yaml
        ('without-interpreters', False),
        # Test Case 4: pytest-fixture.yaml
        ('tests/data/pytest-fixture.yaml', False),
    ],
    ids=[
        'biskotaki',
        'None',
        'without-interpreters',
        'pytest-fixture',
    ],
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
    get_expected_generated_files,
    project_files,
    isolated_cli_runner,
    tmp_path,
):
    from os import path

    # GIVEN the CLI main entrypoint
    from cookiecutter_python.cli import main as cli_main

    # GIVEN a way to compute expectatoins, either in case
    #  - user config yaml, was passed as input to the CLI
    #  - or in case no yaml, but default config was passed as input to the CLI
    config = user_config[config_file]

    # GIVEN that there is not Regression in test code
    assert config.data['project_type'] in {'module', 'module+cli', 'pytest-plugin'}

    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    args, kwargs = cli_invoker_params(
        optional_cli_args={
            '--no-input': True,
            '--config-file': config.config_file,
            '--output-dir': gen_proj_dir,
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
    assert gen_proj_dir.exists()

    project_dir: str = path.abspath(path.join(gen_proj_dir, config.project_slug))

    assert_files_committed_if_flag_is_on(gen_proj_dir, config)

    # Assert Files found at runtime in Generated Project Root Dir are the expected ones
    runtime_generated_files = set(project_files(project_dir).relative_file_paths())

    expected_gen_files: t.Set[Path] = set(get_expected_generated_files(config))

    # TODO: obviously, remove if, with deterministic test config to control all aspect of Logs
    if Path('cookie-py.log') in runtime_generated_files:
        runtime_generated_files.remove(Path('cookie-py.log'))
        logger.warning(
            "Test code issue: cookie-py.log found in set of files, reported by the test code that reads the runtime directory of Gen Proj Dir"
        )
    assert runtime_generated_files == expected_gen_files

    # disable hard-bypass of error/bug
    # assert not path.exists(path.join(project_dir, 'cookie-py.log')), f"Gen Logs Found in Gen Target Dir! File Contents as string:\n\n{open(path.join(project_dir, 'cookie-py.log')).read()}"

    package_exists_on_pypi = check_pypi_result(result.stdout)
    assert package_exists_on_pypi == check_web_server_expected_result('pypi')(
        config, FOUND_ON_PYPI
    )

    package_exists_on_readthedocs = check_readthedocs_result(result.stdout)
    assert package_exists_on_readthedocs == check_web_server_expected_result('readthedocs')(
        config, FOUND_ON_READTHEDOCS
    )


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
