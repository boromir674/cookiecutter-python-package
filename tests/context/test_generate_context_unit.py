"""Unit test for generate_context function - pure function testing.

Although generate_context is a critical function, it is not called by our app
directly. This meanis
"""

import datetime
import typing as t
from collections import OrderedDict

from cookiecutter.generate import generate_context


C_KEY = 'cookiecutter'  # COOKIECUTTER_KEY
_C_KEY = '_cookiecutter'
RELEASE_DATE = datetime.datetime.now().strftime('%Y-%m-%d')


# Use the existing template_test_case fixture - no parametrization needed!
# The fixture already has multiple test cases built-in
def test_generate_context_returns_expected_structure(
    template_test_case,
    tmp_path,
):
    """Test that generate_context returns the expected context structure.

    This is a pure unit test that verifies generate_context output
    without any cookiecutter execution or mocking side effects.
    """
    # GIVEN: Template configuration and user config
    from cookiecutter.config import get_config

    expected_default_context_passed: t.Dict = get_config(template_test_case['user_config'])[
        'default_context'
    ]
    expected_extra_context_passed = None  # as per original test

    # WHEN: We call generate_context directly
    result = generate_context(
        context_file=str(template_test_case['cookie'] / 'cookiecutter.json'),
        default_context=expected_default_context_passed,
        extra_context=expected_extra_context_passed,
    )

    # THEN: The context dict contains only the 'cookiecutter' key (no '_cookiecutter' yet)
    assert isinstance(result, OrderedDict)
    assert set(result.keys()) == {'cookiecutter'}

    # AND: The cookiecutter section is an OrderedDict with expected structure
    assert isinstance(result['cookiecutter'], OrderedDict)

    # AND Choice variables are (still) lists (downstream cookiecutter will pick one later, which is tested in other test module))

    # AND the internal data in jinja context map under 'cookiecutter' key are as expected
    # GIVEN the EXPECTED CONTEXT DISCTIONARY
    EXPECTED_CONTEXT = template_test_case['get_expected_context'](tmp_path)

    # THEN the production generate_context call returns expected Context
    assert result[C_KEY] == EXPECTED_CONTEXT[_C_KEY]
