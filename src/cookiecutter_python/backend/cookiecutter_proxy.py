import json
import logging
import os

from cookiecutter.main import cookiecutter as cookiecutter_main_handler
from software_patterns import Proxy, ProxySubject

from .singleton import Singleton

__all__ = ['cookiecutter']

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


class CookiecutterSubject(ProxySubject[str]):
    pass


class CookiecutterProxy(Proxy[str]):
    def request(self, *args, **kwargs) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        logger.info(
            'Cookiecutter invocation: %s',
            json.dumps(
                {
                    'args': '[{arg_values}]'.format(
                        arg_values=', '.join([f"'{str(x)}'" for x in args])
                    ),
                    'kwargs': '{{{key_value_pairs}}}'.format(
                        key_value_pairs=json.dumps({k: str(v) for k, v in kwargs.items()})
                    ),
                }
            ),
        )
        output_dir: str = super().request(*args, **kwargs)
        return output_dir


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
