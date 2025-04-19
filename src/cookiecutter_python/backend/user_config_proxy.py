import logging
import os
from typing import Any, MutableMapping

from cookiecutter.config import get_user_config as cookie_get_config
from software_patterns import ProxySubject, Singleton

from .proxy import BaseProxy


__all__ = ['get_user_config']


logger = logging.getLogger(__name__)


my_dir = os.path.dirname(os.path.realpath(__file__))


ReturnValueType = MutableMapping[str, Any]


class GetUserConfigSubject(ProxySubject[ReturnValueType]):
    pass


class GetUserConfigProxy(BaseProxy[ReturnValueType]):
    def request(self, *args, **kwargs):
        logger.info(
            *BaseProxy.log_info_args('Get User Config Proxy Request: %s', *args, **kwargs)
        )
        return super().request(*args, **kwargs)


# Singleton and Adapter of cookiecutter.config.get_user_config
class GetUserConfigProxySingleton(metaclass=Singleton):
    def __init__(self, proxy_factory) -> None:
        super().__init__()
        self._proxy = proxy_factory()

    def __call__(self, *args: Any, **kwds: Any) -> ReturnValueType:
        return self._proxy.request(*args, **kwds)


get_user_config = GetUserConfigProxySingleton(
    lambda: GetUserConfigProxy(GetUserConfigSubject(cookie_get_config))
)
