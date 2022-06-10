import logging
from typing import Pattern

from ..input_sanitization import Sanitize
from .base_sanitizer import BaseSanitizer

__all__ = ['BaseSanitizer', 'InputValueError']


logger = logging.getLogger(__name__)


class RegExSanitizer:
    regex: Pattern
    sanitizer: BaseSanitizer

    def __call__(self, data):
        self.sanitizer(data)

    def __init__(self):
        sanitize_data = type(self)
        self.regex = sanitize_data.regex
        self.sanitizer = BaseSanitizer(
            self._verify,
            sanitize_data.exception_msg if sanitize_data.exception_msg else '',
            sanitize_data.log_message,
        )

    def _verify(self, string: str):
        try:
            self.__verify(string)
        except RegExMissMatchError as not_matching_regex:
            raise InputValueError(self.sanitizer.exception_msg) from not_matching_regex

    def __verify(self, string: str):
        if not self.regex.match(string):
            msg = "RegEx Miss Match Error"
            logger.error(*self.sanitizer.log_message(msg, string))
            raise RegExMissMatchError(msg)


class RegExMissMatchError(Exception):
    pass


@Sanitize.register_exception('module-name')
@Sanitize.register_exception('semantic-version')
class InputValueError(Exception):
    pass
