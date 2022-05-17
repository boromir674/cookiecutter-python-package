import typing as t

T = t.TypeVar('T')


class Singleton(type):
    """Singleton Metaclass.

    Example:

        >>> class ObjectDict(metaclass=Singleton):
        ...  def __init__(self):
        ...   super().__init__()
        ...   self.objects = {}

        >>> reg1 = ObjectDict()
        >>> reg1.objects['a'] = 1

        >>> reg2 = ObjectRegistry()
        >>> reg2.objects['b'] = 2

        >>> reg3 = ObjectRegistry()


        >>> reg2.objects == {'a': 1}
        True

        >>> reg3.objects['a'] == 1
        True

        >>> reg3.objects['b'] == 2
        True

        >>> id(reg1) == id(reg2) == id(reg3)
        True
    """

    _instances: t.Dict[t.Type, t.Any] = {}

    def __call__(cls: t.Type, *args, **kwargs) -> t.Any:
        instance = cls._instances.get(cls)
        if not instance:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return instance
