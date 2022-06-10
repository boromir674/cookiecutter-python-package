import logging
import typing as t

logger = logging.getLogger(__name__)

SanitizerLike = t.Callable[[t.Any], None]


class Sanitize:
    exceptions_map: t.Mapping[str, t.Union[t.Type[Exception], t.Tuple]] = {}
    sanitizers_map: t.Mapping[str, SanitizerLike] = {}

    def __getitem__(cls, item) -> SanitizerLike:
        return cls.sanitizers_map[item]

    @property
    def exceptions(self):
        return self.exceptions_map

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
            if isinstance(cls.exceptions_map.get(sanitizer_identifier, None), tuple):
                cls.exceptions_map[sanitizer_identifier] = tuple(list(cls.exceptions_map[sanitizer_identifier]) + [exception_class])
            else:
                cls.exceptions_map[sanitizer_identifier] = exception_class
            return exception_class

        return wrapper


sanitize = Sanitize()
