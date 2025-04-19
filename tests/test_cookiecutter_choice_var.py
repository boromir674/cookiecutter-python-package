from pathlib import Path
from unittest.mock import patch


my_dir = Path(__file__).parent


@patch('cookiecutter.main.generate_context')
def test_calling_cookiecutter_on_prod_template_with_mkdocs_builder(
    generate_context_mock,
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

    # assert yaml.safe_load(config_yaml.read_text())['default_context']['docs_builder'] == 'mkdocs'
    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    # GIVEN a way to "track" the input passed at runtime to cookiecutter's generate_context function
    expected_context_file_passed = str(distro_loc / 'cookiecutter.json')
    from cookiecutter.config import get_config

    user_config_dict = get_config(config_yaml)
    expected_default_context_passed = user_config_dict['default_context']
    # assert expected_default_context_passed['docs_builder'] == 'mkdocs'
    expected_extra_context_passed = None
    if 'interpreters' in user_config_dict:
        expected_extra_context_passed = {'interpreters': user_config_dict['interpreters']}

    # Track the Jinja Context for SANITY Check
    from cookiecutter.generate import generate_context

    prod_result = generate_context(
        context_file=expected_context_file_passed,
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
    )
    # assert prod_result['cookiecutter']['docs_builder'] == ['sphinx', 'mkdocs']

    # WHEN we call cookiecutter with the config file

    generate_context_mock.return_value = prod_result

    project_dir = _cookiecutter(
        cookiecutter,  # template dir path
        # project_dir = generate(
        config_file=str(config_yaml),
        default_config=False,
        extra_context=None,
        output_dir=str(gen_proj_dir),
        no_input=True,  # non interactive
        checkout=None,
        replay=False,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
        password=None,
        directory=None,
    )

    gen_proj: Path = Path(project_dir)

    # SANITY Check that Jinja Context was set properly
    # AND we check the runtime input passed to cookiecutter's generate_context function
    assert generate_context_mock.call_count == 1
    generate_context_mock.assert_called_once()
    # THEN the generate_context was called with expected runtime values
    # assert expected_default_context_passed['docs_builder'] == 'mkdocs'

    generate_context_mock.assert_called_with(
        context_file=expected_context_file_passed,
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
        # extra_context=None,
    )
    assert prod_result['_cookiecutter']['docs_builder'] == ['mkdocs', 'sphinx']
    assert prod_result['cookiecutter']['docs_builder'] == 'mkdocs'

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

    # assert yaml.safe_load(config_yaml.read_text())['default_context']['docs_builder'] == 'mkdocs'
    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    # WHEN we call cookiecutter with the config file
    project_dir = _cookiecutter(
        str(cookie),  # template dir path
        config_file=str(config_yaml),
        default_config=False,
        output_dir=str(gen_proj_dir),
        extra_context=None,
        no_input=True,  # non interactive
        checkout=None,
        replay=False,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
        password=None,
        directory=None,
    )

    gen_proj: Path = Path(project_dir)

    # THEN the Project (folder) is called as expected
    assert gen_proj.name == 'unit-test-new-project'

    assert (gen_proj / 'a.txt').exists()
    # THEN the Choice Value from User Config YAML overrides the default
    assert (gen_proj / 'a.txt').read_text() == 'ELA\nanother_option\n'
