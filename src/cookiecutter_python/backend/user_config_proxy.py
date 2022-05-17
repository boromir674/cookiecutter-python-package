import os
from typing import Any, MutableMapping

from cookiecutter.config import get_user_config as cookie_get_config
from software_patterns import Proxy, ProxySubject

from .singleton import Singleton

__all__ = ['get_user_config']


my_dir = os.path.dirname(os.path.realpath(__file__))


ReturnValueType = MutableMapping[str, Any]


class GetUserConfigSubject(ProxySubject[ReturnValueType]):
    pass


class GetUserConfigProxy(Proxy[ReturnValueType]):
    pass


# Singleton and Adapter of Cookiecutter Proxy
class GetUserConfigProxySingleton(metaclass=Singleton):
    def __init__(self, proxy_factory) -> None:
        super().__init__()
        self._proxy = proxy_factory()

    def __call__(self, *args: Any, **kwds: Any) -> ReturnValueType:
        return self._proxy.request(*args, **kwds)


get_user_config = GetUserConfigProxySingleton(
    lambda: GetUserConfigProxy(GetUserConfigSubject(cookie_get_config))
)
