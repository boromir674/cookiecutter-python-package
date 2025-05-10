import logging
import typing as t


def test_gen_parametrized_only_from_user_config_defaults_to_sphinx_builder_n_py38_in_rtd_ci(
    tmpdir,
    caplog,
):
    # GIVEN a user config YAML file
    from pathlib import Path

    user_config_yaml: Path = (
        Path(__file__).parent / 'data' / 'biskotaki-with-no-docs-specs.yaml'
    )
    assert user_config_yaml.is_file() and user_config_yaml.exists()

    # GIVEN user does not specify any Docs Settings: Builder, rtd CI Python Version
    import yaml

    user_config: t.Dict[str, t.Any] = yaml.safe_load(user_config_yaml.read_text())
    default_context: t.Dict[str, t.Any] = user_config['default_context']
    assert 'docs_builder' not in default_context
    assert 'rtd_python_version' not in default_context

    # WHEN the generator is called with the user config YAML file
    from cookiecutter_python.backend.main import generate

    # Used for heuristically verifying that User Config, does not include
    # information, needed for the backend to compute the URL, which are prerequisite
    # for any Netowrk Http rquest (ie Futures) to be made.
    # We assume that no other fallback method has been developed yet.
    caplog.set_level(logging.INFO)

    # no mock is needed! Verify no web code is called
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
    # sanity that no http mock is needed

    # check the log output and expect URL resolution to fail, and thus Web
    # Hosting checks to be skipped later
    captured_logs: t.List[str] = caplog.messages

    # For each web checker, URL resolution, attempts to parse User Config

    # We find events, when the User Yaml was parsed, during URL resolut'ion, but
    # found missing the Web Service related required Variable from the 'Context'

    web_checks_logs = [
        x
        for x in captured_logs
        if 'Skipping check of remote server, because of missing context variable' in x
    ]

    # THEN the number of Logs hinting for the number URL resolution failures
    # should be equal to the number of web servers supported by the Generator
    assert (
        len(web_checks_logs) == 2
    ), f"Expected 2 logs, got {len(web_checks_logs)}. Possible unintended Nework communication might happen: from web checks making Future Requests to PyPI for example."

    assert (
        'Skipping check of remote server, because of missing context variable'
        in web_checks_logs[0]
    )
    assert (
        'Skipping check of remote server, because of missing context variable'
        in web_checks_logs[1]
    )

    # We treat this as evidence of preventing all otherwise possible, and bound
    # to otherwise happen, network dependent (ie http) calls

    # IF WE DO NOT REACH HERE, we need to Mock http Network (ie Futures) #

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

    assert generated_project_readthedocs_yaml_content['build']['tools']['python'] == '3.8'
    # Note: Python RTD 3.8 has been default for some time
