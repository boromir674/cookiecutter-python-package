import typing as t
import pytest


def test_registering_multiple_exceptions_under_the_same_type_allows_catching_multiple_errors():

    # GIVEN a Sanitize Task - Type

    # GIVEN a way to register exceptions under this Sanitization Task / Type

    # WHEN we register 2 Exceptions under the same Type

    # THEN we should be able to catch both exceptions, in case of error
    from cookiecutter_python.backend.sanitization.input_sanitization import Sanitize
    from cookiecutter_python.backend.sanitization.string_sanitizers.base_sanitizer import BaseSanitizer
    import json
    import logging
    
    logger = logging.getLogger(__name__)

    # Backend Code
    class SimpleSanization:

        def __call__(self, data):
            self.sanitizer(data)

        def __new__(cls):
            x = super().__new__(cls)
            def _log_message(error, input_data):
                raw_log_args: t.Tuple = cls.log_message(error, input_data)
                return tuple([raw_log_args[0]] + [cls._string(x) for x in raw_log_args[1:]])

            x.sanitizer = BaseSanitizer(
                x._verify,
                'Expected a String with chars [a-z], of at least 1 length',
                _log_message,
            )
            return x

        def _verify(self, string: str):
            try:
                self.__verify(string)
            except (StringWithNoLengthError, StringWithImpropperCharsError) as not_matching_regex:
                raise type(not_matching_regex)(self.sanitizer.exception_msg) from not_matching_regex

        def __verify(self, string: str):
            if len(string) < 1:
                msg = "String With No Length Error"
                logger.error(*self.sanitizer.log_message(msg, string))
                raise StringWithNoLengthError(msg)
            if set(string).difference(set('abcdefghijklmnopqrstuvwxyz')):
                msg = "String With Impropper Chars Error. Only [a-z] are allowed"
                logger.error(*self.sanitizer.log_message(msg, string))
                raise StringWithImpropperCharsError(msg)

        @classmethod
        def log_message(cls, error, module) -> t.Tuple[t.Union[str, t.Mapping], ...]:
            return (
                "%s: %s",
                str(error),
                {
                    # 'module_name_regex': str(cls.regex.pattern),
                    'input_string': str(module),
                },
            )
        @classmethod
        def _string(cls, data) -> str:
            if isinstance(data, str):
                return data
            return json.dumps(data, indent=4, sort_keys=True)


    @Sanitize.register_exception('unit-test-sanitizer')
    class StringWithNoLengthError(Exception):
        pass
    
    @Sanitize.register_exception('unit-test-sanitizer')
    class StringWithImpropperCharsError(Exception):
        pass

    # Client Code
    simple_sanitizer = SimpleSanization()

    @Sanitize.register_sanitizer('unit-test-sanitizer')
    def _sanitize_string(string_value: str) -> None:
        simple_sanitizer(string_value)

    # SANITY StringWithNoLengthError is thrown expectedly / "correctly"
    # we Sanitize a string that has no length, we catch 1st exception
    with pytest.raises(StringWithNoLengthError):
        _sanitize_string('')
    
    # SANITY StringWithImpropperCharsError is thrown expectedly / "correctly"
    # we Sanitize a string with improper characters, we catch 2nd exception
    with pytest.raises(StringWithImpropperCharsError):
        _sanitize_string('123')

    # SANITY Santizer has been registered
    from cookiecutter_python.backend import sanitize
    assert 'unit-test-sanitizer' in sanitize.sanitizers_map
    assert sanitize.sanitizers_map['unit-test-sanitizer']

    # SANITY Production Sanitizers automatically loaded!
    PRODUCTION_SANITIZERS = {
        'module-name',
        'semantic-version',
        'interpreters',
    }
    assert set(sanitize.sanitizers_map.keys()) == {'unit-test-sanitizer'}.union(PRODUCTION_SANITIZERS)

    # SANITY Exceptions have been registered
    assert sanitize.exceptions_map['unit-test-sanitizer'] == [StringWithNoLengthError, StringWithImpropperCharsError]


    class InputSanitizationError(Exception):
        pass

    # WHEN we use the Sanitizer, as it is designed to be used, with empty string

    input_string = ''
    with pytest.raises(InputSanitizationError):
        try:
            sanitize['unit-test-sanitizer'](input_string)
        except sanitize.exceptions['unit-test-sanitizer'] as error:
            logger.warning("Input String Value (format) Error: %s", json.dumps({
                'error': str(error),
                'input_string': input_string,
            }, sort_keys=True, indent=4))
            raise InputSanitizationError(
                f"ERROR: '{input_string}' could not pass Sanitization, due to invalid format."
            ) from error

    # WHEN we use the Sanitizer, on string with non [a-z] characters

    input_string = '123'
    with pytest.raises(InputSanitizationError):
        try:
            sanitize['unit-test-sanitizer'](input_string)
        except sanitize.exceptions['unit-test-sanitizer'] as error:
            logger.warning("Input String Value (format) Error: %s", json.dumps({
                'error': str(error),
                'input_string': input_string,
            }, sort_keys=True, indent=4))
            raise InputSanitizationError(
                f"ERROR: '{input_string}' could not pass Sanitization, due to invalid format."
            ) from error
