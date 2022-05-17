import json
import logging
import re
from abc import ABC
from typing import Any, Callable, Pattern, Tuple

from software_patterns.subclass_registry import SubclassRegistry

logger = logging.getLogger(__name__)


def verify_regex_and_log(message_getter):
    def _verify_regex_and_log(regex: Pattern, string: str):
        if not regex.match(string):
            msg = "RegEx Miss Match Error"
            logger.error(*message_getter(msg, regex, string))
            raise RegExMissMatchError(msg)

    return _verify_regex_and_log


def verify_input_with_regex_callback(verify_callback, exception_message=None):
    def verify_input_with_regex(regex: Pattern, string: str):
        try:
            verify_callback(regex, string)
        except RegExMissMatchError as not_matching_regex:
            raise InputValueError(
                exception_message if exception_message else ''
            ) from not_matching_regex

    return verify_input_with_regex


def get_verify_callback(error_message, log_message_getter):
    def _verify_regex(regex: Pattern, string: str):
        verify_with_regex = verify_input_with_regex_callback(
            verify_regex_and_log(log_message_getter), exception_message=error_message
        )
        verify_with_regex(regex, string)

    return _verify_regex


class SanitizerInterface(ABC):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class AbstractSanitizer(SanitizerInterface):
    regex: Pattern
    exception_msg: str
    verify: Callable[[Any], None]

    def log_message(self, error, data) -> Tuple[str]:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        self.verify(self.regex, *args)


class BaseSanitizer(AbstractSanitizer):
    def __init__(self, regex, exception_msg, log_message):
        self.regex = regex
        self.exception_msg = exception_msg
        self._log_func = log_message
        self.verify = get_verify_callback(
            error_message=self.exception_msg,
            log_message_getter=lambda err, reg, x: self.log_message(err, x),
        )

    def log_message(self, error, data) -> Tuple[str]:
        return self._log_func(error, data)

    @staticmethod
    def from_input_sanitizer_class(sanitizer):
        return BaseSanitizer(sanitizer.regex, sanitizer.exception_msg, sanitizer.log_message)


class SanitizerBuilder:
    @staticmethod
    def build(sanitization_type: str):
        sanitizer_instance = BaseSanitizer.from_input_sanitizer_class(
            InputSanitizer.subclasses[sanitization_type]
        )
        return sanitizer_instance


class InputSanitizer(metaclass=SubclassRegistry):
    pass


@InputSanitizer.register_as_subclass('module-name')
class ModuleNameInputSanitizer(InputSanitizer):
    regex = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]+$')
    exception_msg = 'Expected a valid Python Module name value'

    @classmethod
    def log_message(cls, error, module):
        return (
            "%s: %s",
            str(error),
            json.dumps(
                {
                    'module_name_regex': str(cls.regex.pattern),
                    'module_name': str(module),
                },
                indent=2,
                sort_keys=True,
            ),
        )  # TODO Improvement: add indent & sort (as above) to all log messages


@InputSanitizer.register_as_subclass('semantic-version')
class VersionInputSanitizer(InputSanitizer):
    regex = re.compile(
        r'^(?P<major>0|[1-9]\d*)'
        r'\.'
        r'(?P<minor>0|[1-9]\d*)'
        r'\.'
        r'(?P<patch>0|[1-9]\d*)'
        r'(?:-'
        r'(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+'
        r'(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    )
    exception_msg = 'Expected a Semantic Version value'

    @classmethod
    def log_message(cls, error, string):
        return (
            "%s: %s",
            str(error),
            json.dumps(
                {
                    'semver_regex': str(cls.regex.pattern),
                    'version_string': str(string),
                }
            ),
        )


class RegExMissMatchError(Exception):
    pass


class InputValueError(Exception):
    pass


def build_input_verification(input_verifier_type: str):
    return SanitizerBuilder.build(input_verifier_type)
