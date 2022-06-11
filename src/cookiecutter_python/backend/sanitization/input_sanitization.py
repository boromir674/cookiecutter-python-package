import logging
import typing as t
from functools import cached_property

logger = logging.getLogger(__name__)

SanitizerLike = t.Callable[[t.Any], None]
ExceptionValue = t.Union[t.Type[Exception], t.Tuple]
ExceptionsMapValue = t.List[t.Type[Exception]]


class Sanitize:
    sanitizers_map: t.Dict[str, SanitizerLike] = {}
    exceptions_map: t.Dict[str, ExceptionsMapValue] = {}

    def __getitem__(cls, item) -> SanitizerLike:
        return cls.sanitizers_map[item]

    @cached_property
    def exceptions(self) -> t.Mapping[str, ExceptionValue]:
        return {k: v for k, v in self.__iter_exceptions()}

    def __iter_exceptions(self) -> t.Iterator[t.Tuple[str, ExceptionValue]]:
        for k, v in self.exceptions_map.items():
            exception: ExceptionValue = v[0] if len(v) == 1 else tuple(v)
            yield k, exception

    @classmethod
    def register_sanitizer(cls, sanitizer_identifier: str):
        """Add a callback to the sanitizers' registry.

        Args:
            sanitizer_identifier (str): [description]
        """

        def wrapper(func: SanitizerLike) -> SanitizerLike:
            """Add the decorated callback to the sanitizers' registry.

            Args:
                    func (t.Callable): the callback to add to the registry

                Returns:
                    object: the (sub) class
            """
            cls.sanitizers_map[sanitizer_identifier] = func
            return func

        return wrapper

    @classmethod
    def register_exception(cls, sanitizer_identifier: str):
        """Add an Exception to the sanitizers' expected exceptions registry.

        Args:
            sanitizer_identifier (str): [description]
        """

        def wrapper(exception_class: t.Type[Exception]):
            """Add an Exception to the sanitizers' expected exceptions registry.

            Args:
                func (t.Callable): the callback to add to the registry

            Returns:
                object: the (sub) class
            """
            if sanitizer_identifier not in cls.exceptions_map:
                cls.exceptions_map[sanitizer_identifier] = [exception_class]
            else:
                cls.exceptions_map[sanitizer_identifier].append(exception_class)
            return exception_class

        return wrapper


sanitize = Sanitize()