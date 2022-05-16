import os
from typing import Any, Callable, MutableMapping, Optional

from cookiecutter.config import get_user_config as cookie_get_config
from software_patterns import Proxy, ProxySubject

from .singleton import Singleton

__all__ = ['get_user_config']


my_dir = os.path.dirname(os.path.realpath(__file__))


get_user_config_type = Callable[
    [
        Optional[str],
        Optional[bool],
    ],
    MutableMapping[str, Any],
]


class GetUserConfigSubject(ProxySubject[MutableMapping[str, Any]]):
    pass


class GetUserConfigProxy(Proxy[MutableMapping[str, Any]]):
    pass


# Singleton and Adapter of Cookiecutter Proxy
class GetUserConfigProxySingleton(metaclass=Singleton):
    def __init__(self, proxy_factory) -> None:
        super().__init__()
        self._proxy = proxy_factory()

    def __call__(self, *args: Any, **kwds: Any) -> MutableMapping[str, Any]:
        return self._proxy.request(*args, **kwds)


get_user_config = GetUserConfigProxySingleton(
    lambda: GetUserConfigProxy(GetUserConfigSubject(cookie_get_config))
)
