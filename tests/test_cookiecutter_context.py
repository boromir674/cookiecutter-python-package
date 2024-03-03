import pytest
import typing as t
from pathlib import Path
from unittest.mock import patch
from collections import OrderedDict
import datetime

MY_DIR = Path(__file__).parent

@pytest.fixture(params=[(
    # TEST CASE 1 - Simple Template with Cookiecutter Choice Variable included
    # GIVEN a Cookiecutter Template (cookiecutter.json + jinja Template project)
    MY_DIR / 'data' / 'rendering' / 'only_list_template',
    # GIVEN a User Config YAML
    MY_DIR / 'data' / 'rendering' / 'user_config.yml',
    # THEN expected Context that cookiecutter will generate under the hood is
    OrderedDict([
        ('cookiecutter', OrderedDict([
            ('project_dir_name', 'unit-test-new-project'),
            ('some_setting', 'another_option'),
            # ('_template', str(cookie)),
        ])),
    ]),
),
    (
    # TEST CASE 2 - Production Template included in Distribution
    'PROD_TEMPLATE',
    'BISKOTAKI_CONFIG',
    # EXPECTED CONTEXT
    OrderedDict([
        ('cookiecutter', OrderedDict([
            ('project_name', 'Biskotaki'),
            ('project_type', 'module'),
            ("project_slug", "biskotaki"),
            ("pkg_name", "biskotaki"),
            ("repo_name", "biskotaki"),
            ("readthedocs_project_slug", "biskotaki"),
            ("docker_image", "biskotaki"),
            ("full_name", "Konstantinos Lampridis"),
            ("author", "Konstantinos Lampridis"),
            ("author_email", 'k.lampridis@hotmail.com'),
            ("github_username", 'boromir674'),
            ("project_short_description", "Project generated using https://github.com/boromir674/cookiecutter-python-package"),
            ("pypi_subtitle", "Project generated using https://github.com/boromir674/cookiecutter-python-package"),
            # current date in format '2024-03-04'
            ("release_date", datetime.datetime.now().strftime('%Y-%m-%d')),
            ("year", str(datetime.datetime.now().year)),
            ("version", "0.0.1"),
            ("initialize_git_repo", "no"),
            ("docs_builder", "sphinx"),
            ("rtd_python_version", "3.10"),
            # since the below is expected to be put in the extra context before calling cookiecutter, it gets below the rest of Variables
            ("interpreters", {
                "supported-interpreters": [
                    "3.6",
                    "3.7",
                    "3.8",
                    "3.9",
                    "3.10",
                    "3.11"
                ]
            }),
            # ('_template', str(cookie)),
        ])),
    ]),
),
], ids=(
    'simple_template',  # TEST CASE 1
    'prod_template',  # TEST CASE 2
))
def template_test_case(request, distro_loc: Path,
    mock_check, user_config,  # for mocking future http requests to pypi.org and readthedocs.org
):
    # handles cookiecutters dedicated for testing and the one included in the distribution
    cookiecutter_template: Path = distro_loc if request.param[0] == 'PROD_TEMPLATE' else request.param[0]
    user_config_yaml: Path = MY_DIR / '..' / '.github' / 'biskotaki.yaml' if request.param[1] == 'BISKOTAKI_CONFIG' else request.param[1]
    # Prepare Expected Context, produced at runtime by cookiecutter (under the hood)
    expected_context = request.param[2]
    # manual JSON encoding of 'interpreters', when prod Template + Biskotaki Config
    from cookiecutter_python.backend.load_config import get_interpreters_from_yaml

    interpreters: t.Mapping[str, t.Sequence[str]] = get_interpreters_from_yaml(
        user_config_yaml
    )
    print('\n---\n', interpreters)
    if interpreters:
        assert isinstance(interpreters, dict)
        assert isinstance(interpreters['supported-interpreters'], list)
        assert len(interpreters['supported-interpreters']) > 0
        expected_context['cookiecutter']['interpreters'] = interpreters

    # Add the '_template' key to the expected context, like cookiecutter does
    expected_context['cookiecutter']['_template'] = str(cookiecutter_template)
    if request.param[0] == 'PROD_TEMPLATE':
        assert isinstance(interpreters, dict)
        assert isinstance(interpreters['supported-interpreters'], list)
        assert len(interpreters['supported-interpreters']) > 0
        
        # MOCK NETWORK ACCESS
        FOUND_ON_PYPI = False
        FOUND_ON_READTHEDOCS = False

        # mock_check.config = type('A', (), {'data': {'pypi': 'pkg_name', 'readthedocs': 'readthedocs_project_slug'}})
        mock_check.config = user_config[user_config_yaml]
        mock_check('pypi', FOUND_ON_PYPI)
        mock_check('readthedocs', FOUND_ON_READTHEDOCS)
        
        from cookiecutter_python.backend.main import generate as callback
    else:
        from cookiecutter.main import cookiecutter
        callback = lambda **kwargs: cookiecutter(str(cookiecutter_template), **kwargs)
    return {
        'cookie': cookiecutter_template,
        'user_config': user_config_yaml,
        'expected_context': expected_context,
        'cookiecutter_callback': callback,
    }


@patch('cookiecutter.main.generate_context')
def test_cookiecutter_generates_context_with_expected_values(
    generate_context_mock,
    template_test_case,
    tmp_path: Path,
    # mocker,
    # get_object,
):

    # GIVEN a simple Cookiecutter Template: cookiecutter.json + {{ cookiecutter.project_name }}
    # cookie: Path = MY_DIR / 'data' / 'rendering' / 'only_list_template'
    cookie: Path = template_test_case['cookie']
    # GIVEN a User Config YAML, which overrides a default Choice Variable
    # config_yaml: Path = MY_DIR / 'data' / 'rendering' / 'user_config.yml'
    config_yaml: Path = template_test_case['user_config']

    # import yaml
    # assert yaml.safe_load(config_yaml.read_text())['default_context']['some_setting'] == 'another_option'
    # import json
    # assert json.loads((cookie / 'cookiecutter.json').read_text())['some_setting'] == ['some_option', 'another_option']

    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    # GIVEN a way to "track" the input passed at runtime to cookiecutter's generate_context function

    # Define parameter values expected to be passed at runtime to cookiecutter's generate_context function
    # expected to be passed as kwargs
    expected_context_file_passed = str(cookie / 'cookiecutter.json')
    from cookiecutter.config import get_config
    user_config_dict = get_config(config_yaml)
    expected_default_context_passed = user_config_dict['default_context']

    expected_extra_context_passed = None
    if 'interpreters' in template_test_case['expected_context']['cookiecutter']:
        expected_extra_context_passed = {'interpreters': template_test_case['expected_context']['cookiecutter']['interpreters']}

    from cookiecutter.generate import generate_context
    prod_result = generate_context(
        context_file=expected_context_file_passed,
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
    )
    # assert prod_result == OrderedDict([
    #     ('cookiecutter', OrderedDict([
    #         ('project_dir_name', 'unit-test-new-project'),
    #         # OPTIONS SWAP POSITIONS first !! and then picked auto or after interactive promt!
    #         ('some_setting', ['another_option', 'some_option']),
    #     ])),
    # ])

    # assert prod_result == template_test_case['expected_context']

    # WHEN the cookiecutter callable is called on the Tempalte and with the User Config YAML
    generate_context_mock.return_value = prod_result
    project_dir = template_test_case['cookiecutter_callback'](
        # str(cookie),  # template dir path
        config_file=str(config_yaml),
        default_config=False,
        output_dir=gen_proj_dir,
        # extra_context={'interpreters': template_test_case['expected_context']['cookiecutter']['interpreters']} if 'interpreters' in template_test_case['expected_context']['cookiecutter'] else None,
        no_input=True,  # non interactive
        checkout=False,
        replay=False,
    )
    # AND we check the runtime input passed to cookiecutter's generate_context function
    assert generate_context_mock.call_count == 1
    generate_context_mock.assert_called_once()

    # THEN the generate_context was called with expected runtime values  
    generate_context_mock.assert_called_with(
        context_file=expected_context_file_passed,
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
    )

    # SANITY
    # Cookiecutter 1.x
    import poyo
    assert expected_default_context_passed == OrderedDict(
        [(k, v) for k, v in poyo.parse_string(config_yaml.read_text())['default_context'].items()]
    )
    # Cookiecutter 2.x
    # assert expected_default_context_passed == yaml.safe_load(config_yaml.read_text())['default_context']

    # in cookiecutter CONTEXT is an OrderedDict with:
    # - 'cookiecutter': OrderedDict of Template Variables public and private + _template key

    assert prod_result == template_test_case['expected_context']
    assert generate_context_mock.return_value == template_test_case['expected_context']
    # SANITY that Choice Variable was Overriden and that _template get inserted too
    # assert prod_result == OrderedDict([
    #     ('cookiecutter', OrderedDict([
    #         ('project_dir_name', 'unit-test-new-project'),
    #         ('some_setting', 'another_option'),
    #         ('_template', str(cookie)),
    #     ])),
    # ])