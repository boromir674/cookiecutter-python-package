from pathlib import Path


my_dir = Path(__file__).parent


def test_calling_cookiecutter_on_prod_template_with_mkdocs_builder(
    distro_loc: Path,
    tmp_path: Path,
):

    # GIVEN the cookiecutter callable
    from cookiecutter.main import cookiecutter as _cookiecutter

    # GIVEN our Production Template
    cookiecutter: str = str(distro_loc)
    """cookiecutter.json and {{ cookiecutter.pkg_name }} dirs are inside"""

    # GIVEN a config file with 'mkdocs' selection/override for docs_builder
    config_yaml: Path = my_dir / 'data' / 'pytest-fixture.yaml'
    assert config_yaml.exists()
    assert config_yaml.is_file()
    import yaml
    assert yaml.safe_load(config_yaml.read_text())['default_context']['docs_builder'] == 'mkdocs'

    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    # WHEN we call cookiecutter with the config file
    project_dir = _cookiecutter(
        cookiecutter,  # template dir path
        config_file=str(config_yaml),
        # default_config=False,
        output_dir=gen_proj_dir,

        no_input=True,  # non interactive
        checkout=False,
        replay=False,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
    )

    gen_proj: Path = Path(project_dir)

    # THEN we should see the mkdocs.yml file in the output
    assert (gen_proj / 'docs').exists()
    assert (gen_proj / 'mkdocs.yml').exists()


def test_calling_cookiecutter_on_simple_template_with_choice_var(
    tmp_path: Path,
):

    # GIVEN the cookiecutter callable
    from cookiecutter.main import cookiecutter as _cookiecutter

    # GIVEN a cookiecutter Template
    cookie: Path = my_dir / 'data' / 'rendering' / 'only_list_template'

    # GIVEN a config file with 'mkdocs' selection/override for docs_builder
    config_yaml: Path = my_dir / 'data' / 'rendering' / 'user_config.yml'
    assert config_yaml.exists()
    assert config_yaml.is_file()
    import yaml
    # assert yaml.safe_load(config_yaml.read_text())['default_context']['docs_builder'] == 'mkdocs'

    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    # WHEN we call cookiecutter with the config file
    project_dir = _cookiecutter(
        str(cookie),  # template dir path
        config_file=str(config_yaml),
        default_config=False,
        output_dir=gen_proj_dir,
        extra_context=None,

        no_input=True,  # non interactive
        checkout=False,
        replay=False,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
    )

    gen_proj: Path = Path(project_dir)

    # THEN the Project (folder) is called 'another_project'
    assert gen_proj.name == 'unit-test-new-project'

    # AND inside a a.txt file with content 'ELA\nanother_option\n'
    assert (gen_proj / 'a.txt').exists()
    # assert (gen_proj / 'a.txt').read_text() == 'ELA\nMKDOCS SELECTED\n'
    assert (gen_proj / 'a.txt').read_text() == 'ELA\nanother_option\n'
    # assert 0