import typing as t
from abc import ABC, abstractmethod

import attr


class SanitizerInterface(ABC):
    """Sanitizer for the Generator Input Parameters."""

    def __call__(self, data: t.Any) -> None:
        """Sanitize input data.

        Verifies that the input data have a valid value and/or format. Raises an
        exception, if the data do pass the check(s).
        """
        raise NotImplementedError


class AbstractSanitizer(SanitizerInterface, ABC):
    verify: t.Callable[[t.Any], None]
    exception_msg: str

    @abstractmethod
    def log_message(self, error, data) -> t.Tuple:
        raise NotImplementedError

    def __call__(self, data):
        self.verify(data)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class BaseSanitizer(AbstractSanitizer):
    verify: t.Callable[[t.Any], None]
    exception_msg: str
    _log_func: t.Callable[[str, t.Any], t.Tuple]

    def log_message(self, error: str, data) -> t.Tuple:
        return self._log_func(error, data)
