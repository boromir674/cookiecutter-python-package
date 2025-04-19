import json
import logging
import typing as t
from typing import Pattern, Tuple

from ..input_sanitization import Sanitize
from .base_sanitizer import BaseSanitizer


__all__ = ['BaseSanitizer', 'InputValueError']


logger = logging.getLogger(__name__)


class RegExSanitizer:
    regex: t.ClassVar[Pattern]
    sanitizer: t.ClassVar[BaseSanitizer]
    exception_msg: t.ClassVar[str]

    def __call__(self, data):
        self.sanitizer(data)

    @classmethod
    def log_message(cls, error, data) -> t.Tuple:
        raise NotImplementedError

    @classmethod
    def _string(cls, data) -> str:
        if isinstance(data, str):
            return data
        return json.dumps(data, indent=4, sort_keys=True)

    def __init__(self):
        def _log_message(error, input_data):
            raw_log_args: Tuple = type(self).log_message(error, input_data)
            return tuple([raw_log_args[0]] + [self._string(x) for x in raw_log_args[1:]])

        type(self).sanitizer = BaseSanitizer(
            self._verify,
            type(self).exception_msg if type(self).exception_msg else '',
            _log_message,
        )

    def _verify(self, string: str):
        try:
            if not self.regex.match(string):
                msg = "RegEx Miss Match Error"
                logger.error(*self.sanitizer.log_message(msg, string))
                raise RegExMissMatchError(msg)
        except RegExMissMatchError as not_matching_regex:
            raise InputValueError(self.sanitizer.exception_msg) from not_matching_regex


class RegExMissMatchError(Exception):
    pass


@Sanitize.register_exception('module-name')
@Sanitize.register_exception('semantic-version')
class InputValueError(Exception):
    pass
