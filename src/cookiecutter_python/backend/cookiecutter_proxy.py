import json
import logging
import os

from cookiecutter.main import cookiecutter as cookiecutter_main_handler
from software_patterns import Proxy, ProxySubject

from .singleton import Singleton

__all__ = ['cookiecutter']

# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
logging.basicConfig()

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


class CookiecutterSubject(ProxySubject[str]):
    pass


class CookiecutterProxy(Proxy[str]):
    """Proxy to cookiecutter: 'from cookiecutter.main import cookiecutter'."""

    def request(self, *args, **kwargs) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        logger.debug(
            'Cookiecutter Proxy Request: %s',
            json.dumps(
                {
                    'keyword_args': {k: str(v) for k, v in kwargs.items()},
                    'positional_args': [str(arg_value) for arg_value in args],
                },
                indent=2,
                sort_keys=True,
            ),
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
