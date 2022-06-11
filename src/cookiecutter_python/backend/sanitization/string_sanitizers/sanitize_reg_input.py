import json
import logging
from typing import Pattern, Tuple

from ..input_sanitization import Sanitize
from .base_sanitizer import BaseSanitizer

__all__ = ['BaseSanitizer', 'InputValueError']


logger = logging.getLogger(__name__)


class RegExSanitizer:
    regex: Pattern
    sanitizer: BaseSanitizer

    def __call__(self, data):
        self.sanitizer(data)

    @classmethod
    def _string(cls, data) -> str:
        if isinstance(data, str):
            return data
        return json.dumps(data, indent=4, sort_keys=True)

    def __init__(self):
        sanitize_data = type(self)
        self.regex = sanitize_data.regex

        def _log_message(error, input_data):
            raw_log_args: Tuple = sanitize_data.log_message(error, input_data)
            return tuple([raw_log_args[0]] + [self._string(x) for x in raw_log_args[1:]])

        self.sanitizer = BaseSanitizer(
            self._verify,
            sanitize_data.exception_msg if sanitize_data.exception_msg else '',
            _log_message,
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
