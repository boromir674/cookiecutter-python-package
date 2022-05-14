"""Proxy structural software pattern.

This module contains boilerplate code to supply the Proxy structural software
design pattern, to the client code."""

import json
import logging
from typing import Any, Callable, Optional

from cookiecutter.main import cookiecutter as cookiecutter_main_handler
from software_patterns import Proxy, ProxySubject

from .singleton import Singleton

__all__ = ['cookiecutter']

logger = logging.getLogger(__name__)


cookiecutter_type = Callable[
    [
        str,
        Optional[str],
        bool,
        Optional[dict],
        bool,
        bool,
        Optional[str],
        Optional[str],
        bool,
        Optional[str],
        Optional[str],
        bool,
    ],
    str,
]


class CookiecutterSubject(ProxySubject[cookiecutter_type]):
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
    def __init__(self) -> None:
        super().__init__()
        # wrapper around 'proxied' object; cookiecutter in this case
        cookiecutter_subject = CookiecutterSubject(cookiecutter_main_handler)
        self._proxy = CookiecutterProxy(cookiecutter_subject)

    def __call__(self, *args: Any, **kwds: Any) -> str:
        return self._proxy.request(*args, **kwds)


cookiecutter = CookiecutterProxySingleton()
