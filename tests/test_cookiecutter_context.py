import datetime
import typing as t
from collections import OrderedDict
from pathlib import Path
from unittest.mock import patch

import pytest

MY_DIR = Path(__file__).parent
CK = 'cookiecutter'  # COOKIECUTTER_KEY
# offest by 2 hours to match Jinja 'now' expression: {% now 'utc', '%Y-%m-%d' %}
# RELEASE_DATE = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d')
RELEASE_DATE = datetime.datetime.now().strftime('%Y-%m-%d')


@pytest.fixture(
    params=[
        (
            # TEST CASE 1 - Simple Template with Cookiecutter Choice Variable included
            # GIVEN a Cookiecutter Template (cookiecutter.json + jinja Template project)
            MY_DIR / 'data' / 'rendering' / 'only_list_template',
            # GIVEN a User Config YAML
            MY_DIR / 'data' / 'rendering' / 'user_config.yml',
            # THEN expected Context that cookiecutter will generate under the hood is
            OrderedDict(
                [
                    # 1st Item mapped in Jinja context with dedicated key
                    (
                        'cookiecutter',
                        OrderedDict(
                            [
                                ('project_dir_name', 'unit-test-new-project'),
                                ('some_setting', 'another_option'),
                                # ('_template', str(cookie)),
                            ]
                        ),
                    ),
                    # 2nd Item mapped in Jinja context with dedicated key
                    (
                        '_cookiecutter',
                        {
                            'project_dir_name': 'unit-test-new-project',
                            'some_setting': [
                                'another_option',
                                'some_option',
                            ],  # NOTE Difference to 1st Item
                        },
                    ),
                ]
            ),
        ),
        (
            # TEST CASE 2 - Production Template included in Distribution
            'PROD_TEMPLATE',
            'BISKOTAKI_CONFIG',
            # EXPECTED CONTEXT
            OrderedDict(
                [
                    # 1st Item mapped in Jinja context with dedicated key
                    (
                        'cookiecutter',
                        OrderedDict(
                            [
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
                                (
                                    "project_short_description",
                                    "Project generated using https://github.com/boromir674/cookiecutter-python-package",
                                ),
                                (
                                    "pypi_subtitle",
                                    "Project generated using https://github.com/boromir674/cookiecutter-python-package",
                                ),
                                ("release_date", RELEASE_DATE),
                                ("year", str(datetime.datetime.now().year)),
                                ("version", "0.0.1"),
                                ("initialize_git_repo", "no"),
                                (
                                    "interpreters",
                                    {
                                        "supported-interpreters": [
                                            "3.6",
                                            "3.7",
                                            "3.8",
                                            "3.9",
                                            "3.10",
                                            "3.11",
                                        ]
                                    },
                                ),
                                ("docs_builder", "sphinx"),
                                ("rtd_python_version", "3.10"),
                                # since the below is expected to be put in the extra context before calling cookiecutter, it gets below the rest of Variables
                                # ('_template', str(cookie)),
                            ]
                        ),
                    ),
                    # 2nd Item mapped in Jinja context with dedicated key _cookiecutter
                    (
                        '_cookiecutter',
                        {
                            'project_name': 'Biskotaki',
                            'project_type': [
                                'module',
                                'module+cli',
                                'pytest-plugin',
                            ],  # NOTE Difference to 1st Item
                            "project_slug": "biskotaki",
                            "pkg_name": "biskotaki",
                            "repo_name": "biskotaki",
                            "readthedocs_project_slug": "biskotaki",
                            "docker_image": "biskotaki",
                            "full_name": "Konstantinos Lampridis",
                            "author": "Konstantinos Lampridis",
                            "author_email": 'k.lampridis@hotmail.com',
                            "github_username": 'boromir674',
                            # "project_short_description": "Project generated using https://github.com/boromir674/cookiecutter-python-package",
                            "project_short_description": "{{ cookiecutter.project_short_description }}",
                            "pypi_subtitle": "Project generated using https://github.com/boromir674/cookiecutter-python-package",
                            # current date in format '2024-03-04'
                            # "release_date": datetime.datetime.now().strftime('%Y-%m-%d'),
                            "release_date": "{% now 'utc', '%Y-%m-%d' %}",
                            "year": "{% now 'utc', '%Y' %}",
                            "version": "0.0.1",
                            "initialize_git_repo": [
                                'no',
                                'yes',
                            ],  # NOTE Difference to 1st Item
                            "interpreters": {
                                "supported-interpreters": ["3.7", "3.8", "3.9", "3.10", "3.11"]
                            },
                            "docs_builder": [
                                'sphinx',
                                'mkdocs',
                            ],  # NOTE Difference to 1st Item
                            "rtd_python_version": ["3.10", "3.8", "3.9", "3.11", "3.12"],
                        },
                    ),
                ]
            ),
        ),
        (
            # TEST CASE 3 - Production Template + Gold Standard User Config
            'PROD_TEMPLATE',
            'GOLD_STANDARD_CONFIG',
            # EXPECTED CONTEXT
            OrderedDict(
                [
                    # 1st Item mapped in Jinja context with dedicated key
                    (
                        CK,
                        OrderedDict(
                            [
                                ('project_name', 'Biskotaki Gold Standard'),
                                ('project_type', 'module+cli'),
                                ("project_slug", "biskotaki-gold-standard"),
                                ("pkg_name", "biskotakigold"),
                                ("repo_name", "biskotaki-gold"),
                                ("readthedocs_project_slug", "biskotaki-gold"),
                                ("docker_image", "bgs"),
                                ("full_name", "Konstantinos Lampridis"),
                                ("author", "Konstantinos Lampridis"),
                                ("author_email", 'k.lampridis@hotmail.com'),
                                ("github_username", 'boromir674'),
                                (
                                    "project_short_description",
                                    "Project generated from https://github.com/boromir674/cookiecutter-python-package/",
                                ),
                                (
                                    "pypi_subtitle",
                                    "Project generated from https://github.com/boromir674/cookiecutter-python-package/",
                                ),
                                ("release_date", RELEASE_DATE),
                                ("year", str(datetime.datetime.now().year)),
                                ("version", "0.0.1"),
                                ("initialize_git_repo", "no"),
                                (
                                    "interpreters",
                                    {"supported-interpreters": ["3.8", "3.9", "3.10", "3.11"]},
                                ),
                                ("docs_builder", "mkdocs"),
                                ("rtd_python_version", "3.10"),
                            ]
                        ),
                    ),
                    # 2nd Item mapped in Jinja context with dedicated key _cookiecutter
                    (
                        '_cookiecutter',
                        {
                            'project_name': 'Biskotaki Gold Standard',
                            'project_type': [
                                'module+cli',
                                'module',
                                'pytest-plugin',
                            ],  # NOTE Difference to 1st Item
                            "project_slug": "biskotaki-gold-standard",
                            "pkg_name": "biskotakigold",
                            "repo_name": "biskotaki-gold",
                            "readthedocs_project_slug": "biskotaki-gold",
                            "docker_image": "bgs",
                            "full_name": "Konstantinos Lampridis",
                            "author": "Konstantinos Lampridis",
                            "author_email": 'k.lampridis@hotmail.com',
                            "github_username": 'boromir674',
                            # "project_short_description": "Project generated using https://github.com/boromir674/cookiecutter-python-package",
                            "project_short_description": "{{ cookiecutter.project_short_description }}",
                            "pypi_subtitle": "Project generated using https://github.com/boromir674/cookiecutter-python-package",
                            # current date in format '2024-03-04'
                            # "release_date": datetime.datetime.now().strftime('%Y-%m-%d'),
                            # "release_date": RELEASE_DATE,
                            "release_date": "{% now 'utc', '%Y-%m-%d' %}",
                            "year": "{% now 'utc', '%Y' %}",
                            # "year": str(datetime.datetime.now().year),
                            "version": "0.0.1",
                            "initialize_git_repo": [
                                'no',
                                'yes',
                            ],  # NOTE Difference to 1st Item
                            "interpreters": {
                                "supported-interpreters": ["3.8", "3.9", "3.10", "3.11"]
                            },
                            "docs_builder": [
                                'mkdocs',
                                'sphinx',
                            ],  # NOTE Difference to 1st Item
                            "rtd_python_version": ["3.10", "3.8", "3.9", "3.11", "3.12"],
                        },
                    ),
                ]
            ),
        ),
    ],
    ids=(
        'simple_template',  # TEST CASE 1
        'prod_template',  # TEST CASE 2
        'gold_standard',  # TEST CASE 3
    ),
)
def template_test_case(
    request,
    distro_loc: Path,
    mock_check,
    user_config,  # for mocking future http requests to pypi.org and readthedocs.org
):
    # handles cookiecutters dedicated for testing and the one included in the distribution
    cookiecutter_template: Path = (
        distro_loc if request.param[0] == 'PROD_TEMPLATE' else request.param[0]
    )
    user_config_yaml: Path
    # Set User Config YAML
    if request.param[1] == 'BISKOTAKI_CONFIG':
        user_config_yaml = MY_DIR / '..' / '.github' / 'biskotaki.yaml'
    elif request.param[1] == 'GOLD_STANDARD_CONFIG':
        user_config_yaml = MY_DIR / 'data' / 'gold-standard.yml'
    elif request.param[1] == 'PYTEST_PLUGIN_CONFIG':
        user_config_yaml = MY_DIR / 'data' / 'pytest-fixture.yaml'
    else:
        user_config_yaml = request.param[1]

    # Prepare Expected Context, produced at runtime by cookiecutter (under the hood)
    expected_context = request.param[2]

    expected_cookiecutter_parent_dir: str = str(cookiecutter_template)

    # Solve issue of CI Windows, with a hack
    import os
    import sys
    testing_against_sdist: bool = 'PY_SDIST' in os.environ
    if sys.platform == 'win32' and testing_against_sdist:
        # now we allow only the 'expected_cookiecutter_parent_dir' to deviate by 1 letter !!!
        expected_cookiecutter_parent_dir = expected_cookiecutter_parent_dir.replace(
            'lib', 'Lib'
        )

    # include template dir or url in the context dict
    expected_context[CK]['_template'] = expected_cookiecutter_parent_dir

    # include output+dir in the context dict
    # context[CK]['_output_dir'] = os.path.abspath(output_dir)

    # include repo dir or url in the context dict
    expected_context[CK]['_repo_dir'] = expected_cookiecutter_parent_dir

    # include checkout details in the context dict
    expected_context[CK]['_checkout'] = False

    # manual JSON encoding of 'interpreters', when prod Template + Biskotaki Config
    from cookiecutter_python.backend.load_config import get_interpreters_from_yaml

    interpreters = get_interpreters_from_yaml(str(user_config_yaml))

    print('\n---\n', interpreters)
    if interpreters:
        assert isinstance(interpreters, dict)
        assert isinstance(interpreters['supported-interpreters'], list)
        assert len(interpreters['supported-interpreters']) > 0
        expected_context['cookiecutter']['interpreters'] = interpreters

    callback: t.Callable

    # Add the '_template' key to the expected context, like cookiecutter does
    expected_context['cookiecutter']['_template'] = expected_cookiecutter_parent_dir
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

        from cookiecutter_python.backend.main import generate as generate_callback

        callback = generate_callback
    else:
        from cookiecutter.main import cookiecutter

        def _generate_callback(**kwargs):
            return cookiecutter(str(cookiecutter_template), **kwargs)

        callback = _generate_callback

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
    # GIVEN a Cookiecutter Template: Dir with cookiecutter.json + {{ cookiecutter.project_name }}/
    cookie: Path = template_test_case['cookie']
    # GIVEN a User Config YAML, which overrides a default Choice Variable
    config_yaml: Path = template_test_case['user_config']

    # GIVEN target Gen Project dir has no files inside
    gen_proj_dir: Path = tmp_path
    assert gen_proj_dir.exists() and len(list(gen_proj_dir.iterdir())) == 0

    # UPDATE EXPECTATION (todo move outside of this Test Case, into Data block)
    # template_test_case['expected_context'][CK]['_output_dir'] = str(gen_proj_dir.absolute())
    # build new Ordered Dict since _output_dir needs to be between _template and _repo_dir
    def gen():
        # generator keys an inject _output_dir
        for k, v in template_test_case['expected_context'][CK].items():
            # if key is not _template, yield it
            if k != '_template':
                yield k, v
            # if key is _template, yield it and then yield _output_dir
            else:
                yield k, v
                yield '_output_dir', str(gen_proj_dir.absolute())

    patched_CK_context = OrderedDict([(k, v) for k, v in gen()])
    template_test_case['expected_context'][CK] = patched_CK_context

    # GIVEN a way to "track" the input passed at runtime to cookiecutter's generate_context function

    # Define parameter values expected to be passed at runtime to cookiecutter's generate_context function
    # expected to be passed as kwargs
    # str(cookie / 'cookiecutter.json')
    expected_context_file_passed = template_test_case['expected_context']['cookiecutter'][
        '_template'
    ]

    from cookiecutter.config import get_config

    user_config_dict = get_config(config_yaml)
    expected_default_context_passed = user_config_dict['default_context']

    expected_extra_context_passed = None
    if 'interpreters' in template_test_case['expected_context']['cookiecutter']:
        expected_extra_context_passed = {
            'interpreters': template_test_case['expected_context']['cookiecutter'][
                'interpreters'
            ]
        }

    from cookiecutter.generate import generate_context

    prod_result = generate_context(
        context_file=str(cookie / 'cookiecutter.json'),
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
    )

    # assert prod_result == template_test_case['expected_context']

    # WHEN the cookiecutter callable is called on the Tempalte and with the User Config YAML
    generate_context_mock.return_value = prod_result

    template_test_case['cookiecutter_callback'](
        # str(cookie),  # template dir path
        config_file=str(config_yaml),
        default_config=False,
        output_dir=gen_proj_dir,
        # extra_context={'interpreters': template_test_case['expected_context']['cookiecutter']['interpreters']} if 'interpreters' in template_test_case['expected_context']['cookiecutter'] else None,
        no_input=True,  # non interactive
        checkout=False,
        replay=False,
    )
    # SANITY check that Context Generated once
    assert generate_context_mock.call_count == 1
    generate_context_mock.assert_called_once()

    # AND we check the runtime input passed to cookiecutter's generate_context function
    # THEN the generate_context was called with expected runtime values

    generate_context_mock.assert_called_with(
        context_file=str(Path(expected_context_file_passed) / 'cookiecutter.json'),
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
    )

    import yaml

    # SANITY check User Config YAML data passed as Dict to 'default_context' kwarg of generate_context
    assert expected_default_context_passed == OrderedDict(
        [(k, v) for k, v in yaml.safe_load(config_yaml.read_text())['default_context'].items()]
    )
    # AND Cookiecutter inserts 2 keys into Jinja Context: 'cookiecutter' and '_cookiecutter'
    assert set(prod_result.keys()) == {CK, '_cookiecutter'}
    # AND the Template Variables in 'cookiecutter' key is an OrderedDict
    assert isinstance(prod_result[CK], OrderedDict)
    # AND the back-up/copy of raw data is place under '_cookiecutter' key as Dict
    assert isinstance(prod_result['_cookiecutter'], dict)

    # SANITY
    assert len(prod_result[CK]) == len(template_test_case['expected_context'][CK])
    for p1, p2 in zip(
        prod_result[CK].items(), template_test_case['expected_context'][CK].items()
    ):
        assert p1[0] == p2[0], (
            "All PROD Keys: [\n"
            + '\n'.join(prod_result[CK].keys())
            + '\n]\n\nAll TEST Keys: [\n'
            + '\n'.join(template_test_case['expected_context'][CK].keys())
            + "\n]"
        )
        assert (
            p1[1] == p2[1]
        ), f"Context Missmatch at '{CK}' -> '{p1[0]}': Runtime: '{p1[1]}', Expected: '{p2[1]}'"

    assert prod_result[CK] == template_test_case['expected_context'][CK]

    # SANITY
    assert len(prod_result['_cookiecutter']) == len(
        template_test_case['expected_context']['_cookiecutter']
    )
    for p1, p2 in zip(
        prod_result['_cookiecutter'].items(),
        template_test_case['expected_context']['_cookiecutter'].items(),
    ):
        assert p1[0] == p2[0]
        if p1[0] in {'project_short_description', 'pypi_subtitle'}:
            continue
        assert p1[1] == p2[1], f"Error at key {p1[0]} with value {p1[1]}! Expected {p2[1]}!"
