import logging
import os

from cookiecutter.main import cookiecutter as cookiecutter_main_handler
from software_patterns import ProxySubject, Singleton

from ..proxy import BaseProxy


__all__ = ['cookiecutter']


logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


class CookiecutterSubject(ProxySubject[str]):
    pass


class CookiecutterProxy(BaseProxy[str]):
    """Proxy to cookiecutter: 'from cookiecutter.main import cookiecutter'."""

    def request(self, *args, **kwargs) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        logger.info(
            *BaseProxy.log_info_args('Cookiecutter Proxy Request: %s', *args, **kwargs)
        )
        return super().request(*args, **kwargs)


# Singleton and Adapter of Cookiecutter Proxy
class CookiecutterProxySingleton(metaclass=Singleton):
    def __init__(self, proxy_factory) -> None:
        super().__init__()
        self._proxy = proxy_factory()

    def __call__(self, *args, **kwds) -> str:
        return self._proxy.request(*args, **kwds)


cookiecutter = CookiecutterProxySingleton(
    lambda: CookiecutterProxy(CookiecutterSubject(cookiecutter_main_handler))
)

generator = cookiecutter
