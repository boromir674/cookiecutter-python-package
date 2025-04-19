import logging
import typing as t


logger = logging.getLogger(__name__)

SanitizerLike = t.Callable[[t.Any], None]
ExceptionValue = t.Union[t.Type[Exception], t.Tuple]
ExceptionsMapValue = t.List[t.Type[Exception]]


class Sanitize:
    sanitizers_map: t.Dict[str, SanitizerLike] = {}
    exceptions_map: t.Dict[str, ExceptionsMapValue] = {}

    def __getitem__(self, item) -> SanitizerLike:
        return self.sanitizers_map[item]

    @property
    def exceptions(self) -> t.Mapping[str, ExceptionValue]:
        return dict(self.__iter_exceptions())

    def __iter_exceptions(self) -> t.Iterator[t.Tuple[str, ExceptionValue]]:
        for key, exceptions_list in self.exceptions_map.items():
            exception: ExceptionValue = (
                exceptions_list[0] if len(exceptions_list) == 1 else tuple(exceptions_list)
            )
            yield key, exception

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
