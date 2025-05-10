import sys
import typing as t


if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import pytest


CookiecutterJSONDefaults = t.Dict[str, t.Any]


class ParsedConfig(Protocol):
    data: CookiecutterJSONDefaults


@pytest.fixture
def distro_gen_docs_defaults(
    user_config,
    # ) -> t.TypedDict[
    #     'docs_builder': str,
    #     'rtd_python_version': str,
    # ]:
):
    """The officially recognized defaults for the Docs Generator Feature.

    Confidentlly, advertize that this is the default, which the generator will use,
    in case the user does not provide any input, for the Docs Generator Feature.
    """
    # Read Gen Doc Defaults Settings from cookiecutter.json
    # we leverage user_config, to avoid potentially having to jinja render templated text
    config: ParsedConfig = user_config[None]
    # config: ParsedConfig = user_config[distro_loc / 'cookiecutter.json']
    # default Docs Builder (ie mkdocs, sphinx)
    docs_builder: str = config.data['docs_builder']
    # for legacy and backwards-compatibility reasons we have sphinx as default
    GENERATOR_DEFAULT_DOCS_BUILDER: str = 'sphinx'
    assert docs_builder == GENERATOR_DEFAULT_DOCS_BUILDER, (
        f"Expected 'sphinx' as default docs_builder, but got '{docs_builder}'.\n"
        " In case the change is intended, then arguably it causes a 'public API' change, which indicates a 'breaking change'. So, whenever it is released, it should cause a Major Sev Ver bump.\n"
        " So, to fix, update GENERATOR_DEFAULT_DOCS_BUILDER variable, to match the new default. and make a Major release, when the time comes!\n"
        " In case the change is not intended, then it is a bug, and this test properly sptoted the regression.\n"
        " To fix, you probably need to inspect the cookiecutters.json file, and see why the default changed.\n"
    )
    # default Python interpreter installed in rtd CI Job runner
    rtd_py_version: str = config.data['rtd_python_version']
    # for backwards-compatibility reasons we have '3.8' Python as default
    GENERATOR_DEFAULT_RTD_PYTHON_VERSION: str = '3.8'
    assert rtd_py_version == GENERATOR_DEFAULT_RTD_PYTHON_VERSION, (
        f"Expected '3.8' as default rtd_python_version, but got '{rtd_py_version}'.\n"
        " In case the change is intended, then arguably it causes a 'public API' change, which indicates a 'breaking change'. So, whenever it is released, it should probably cause a Major Sev Ver bump.\n"
        " So, to fix, update GENERATOR_DEFAULT_RTD_PYTHON_VERSION variable, to match the new default. and make a Major release, when the time comes!\n"
        " In case the change is not intended, then it is a bug, and this test properly sptoted the regression.\n"
        " To fix, you probably need to inspect the cookiecutters.json file, and see why the default changed.\n"
    )
    return {
        'docs_builder': docs_builder,
        'rtd_python_version': rtd_py_version,
    }


def test_gen_parametrized_only_from_user_config_defaults_to_sphinx_builder_n_py38_in_rtd_ci(
    distro_gen_docs_defaults,  # 'official' Docs Context Defaults, as defined in cookiecutter.json
    mock_check,  # allows mocking potential network calls, made by 'web checks' feature
    # derives Template Variables, able to parse User (yaml) and Default (json) Config
    user_config,  # automatically derives runtime values, when encountering Templated Code (ie jinja templated parts in cookicutter json)
    tmpdir,
):
    # GIVEN a user config YAML file
    from pathlib import Path

    user_config_yaml: Path = (
        Path(__file__).parent.parent / 'data' / 'biskotaki-with-no-docs-specs.yaml'
    )
    assert user_config_yaml.is_file() and user_config_yaml.exists()

    # WHEN generator called with input the user config YAML file, and no default config
    from cookiecutter_python.backend.main import generate

    # AND we prevent any network bound calls, by inserting emulated results
    # parse user config yaml data, into same Dict schema, which the generator would
    # have parsed to attempt gathering the required information for URL resolution
    config = user_config[user_config_yaml]

    # the below allows URL resolutoin, same as in prod, (ie same bug should appear, if syntax error in user yaml)
    # and also allow mocking the 'web checks' feature, which is enabled automatically and independently, per web hosting service,
    mock_check.config = config

    # Emulate Asynchronous (Future) Responses, in case 'web checks' feature is enabled
    # feature is enabled automatically and independently, per web hosting service,
    # in case it finds all the required information, whn doing URL resolution

    # we make sure no network calls are made, independently of URL resolution!

    # Emulate Asynchronous (Future) Response, as if, no name collision would
    # happen for 'PyPI'
    mock_check('pypi', False)
    # Emulate Asynchronous (Future) Response, as if, no name collision would
    # happen for 'Read The Docs'
    mock_check('readthedocs', False)

    project_dir: str = generate(
        checkout=None,
        no_input=True,
        replay=False,
        overwrite=False,
        output_dir=tmpdir,
        config_file=str(user_config_yaml),
        default_config=False,
        password=None,
        directory=None,
        skip_if_file_exists=False,
    )
    # THEN the generator should have fallen back to the DOCS Template Defaults

    from pathlib import Path

    generated_project_dir: Path = Path(project_dir)
    assert generated_project_dir.is_dir() and generated_project_dir.exists()

    # AND is Sphinx is verified as the default Docs Builder
    ## default Docs Builder is Sphinx (same as when doc builder did not allow user other options)
    assert (generated_project_dir / 'docs' / 'conf.py').is_file()

    # AND Python Version 3.8 is verified as the default rtd CI Python Version
    ## default RTD Python Version is 3.8 (same as when only shinx was only doc builder option)
    import yaml

    generated_project_readthedocs_yaml_content: t.Dict[str, t.Any] = yaml.safe_load(
        (generated_project_dir / '.readthedocs.yml').read_text()
    )
    assert 'build' in generated_project_readthedocs_yaml_content
    assert 'tools' in generated_project_readthedocs_yaml_content['build']
    assert 'python' in generated_project_readthedocs_yaml_content['build']['tools']

    assert (
        generated_project_readthedocs_yaml_content['build']['tools']['python']
        == distro_gen_docs_defaults['rtd_python_version']
    )
    # Note: Python RTD 3.8 has been default for some time
