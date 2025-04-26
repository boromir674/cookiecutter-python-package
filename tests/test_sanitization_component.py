import pytest


@pytest.fixture
def real_scenario():
    # GIVEN a Sanitize Task - Type
    SANITIZE_TASK_TYPE = 'unit-test-sanitizer'

    # GIVEN the official way of a Registering a Sanitizer Task / Type
    from cookiecutter_python.backend.sanitization.input_sanitization import Sanitize

    # Backend Code that declares and registers a new Sanitizer
    @Sanitize.register_sanitizer(SANITIZE_TASK_TYPE)
    def verify_input_string_not_empty_and_only_lowercase_latin_chars(
        string: str,
    ) -> None:
        if len(string) < 1:
            raise StringWithNoLengthError("String With No Length Error")

        if set(string).difference(set('abcdefghijklmnopqrstuvwxyz')):
            raise StringWithImpropperCharsError(
                "String With Impropper Chars Error. Only [a-z] are allowed"
            )

    # GIVEN a way to register exceptions under this Sanitization Task / Type

    @Sanitize.register_exception(SANITIZE_TASK_TYPE)
    class StringWithNoLengthError(Exception):
        pass

    # WHEN we register 2 Exceptions under the same Type
    @Sanitize.register_exception(SANITIZE_TASK_TYPE)
    class StringWithImpropperCharsError(Exception):
        pass

    # SANITY Santizer has been registered
    from cookiecutter_python.backend import sanitize

    assert SANITIZE_TASK_TYPE in sanitize.sanitizers_map
    assert sanitize.sanitizers_map[SANITIZE_TASK_TYPE]  # type:ignore[truthy-function]

    # SANITY Production Sanitizers automatically loaded!
    PRODUCTION_SANITIZERS = {
        'module-name',
        'semantic-version',
        'interpreters',
    }
    assert set(sanitize.sanitizers_map.keys()) == {SANITIZE_TASK_TYPE}.union(
        PRODUCTION_SANITIZERS
    )

    # SANITY Exceptions have been registered
    assert sanitize.exceptions_map[SANITIZE_TASK_TYPE] == [
        StringWithNoLengthError,
        StringWithImpropperCharsError,
    ]

    # SANITY StringWithNoLengthError is thrown expectedly / "correctly"
    # we Sanitize a string that has no length, we catch 1st exception
    with pytest.raises(StringWithNoLengthError):
        verify_input_string_not_empty_and_only_lowercase_latin_chars('')

    # SANITY StringWithImpropperCharsError is thrown expectedly / "correctly"
    # we Sanitize a string with improper characters, we catch 2nd exception
    with pytest.raises(StringWithImpropperCharsError):
        verify_input_string_not_empty_and_only_lowercase_latin_chars('123')


def test_registering_multiple_exceptions_under_the_same_type_allows_catching_multiple_errors(
    real_scenario,  # proves that "client-code" does not need to reference the exceptions
    # but the exceptions are registered under the same type, so we can catch them
):
    # THEN we should be able to catch both exceptions, in case of error
    class InputSanitizationError(Exception):
        pass

    # SANITY Santizer has been registered
    from cookiecutter_python.backend import sanitize

    # GIVEN a Sanitize Task - Type
    SANITIZE_TASK_TYPE = 'unit-test-sanitizer'

    # WHEN we use the Sanitizer, with empty string
    input_string = ''
    with pytest.raises(InputSanitizationError):
        try:
            sanitize[SANITIZE_TASK_TYPE](input_string)
        except sanitize.exceptions[SANITIZE_TASK_TYPE] as error:
            raise InputSanitizationError(
                f"ERROR: '{input_string}' could not pass Sanitization, due to invalid format."
            ) from error

    # WHEN we use the Sanitizer, on string with non [a-z] characters
    input_string = '123'
    with pytest.raises(InputSanitizationError):
        try:
            sanitize[SANITIZE_TASK_TYPE](input_string)
        except sanitize.exceptions[SANITIZE_TASK_TYPE] as error:
            raise InputSanitizationError(
                f"ERROR: '{input_string}' could not pass Sanitization, due to invalid format."
            ) from error
