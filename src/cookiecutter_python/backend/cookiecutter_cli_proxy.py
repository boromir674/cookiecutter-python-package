"""Proxy structural software pattern.

This module contains boilerplate code to supply the Proxy structural software
design pattern, to the client code."""

from typing import Callable, Any, Optional
import json
import logging

from software_patterns import Proxy
from software_patterns import ProxySubject
from cookiecutter.cli import main as cookiecutter_main

from .singleton import Singleton

__all__ = ['cookiecutter_main']

logger = logging.getLogger(__name__)


cookiecutter_main_type = Callable


class CookiecutterMainSubject(ProxySubject[cookiecutter_main_type]):
    pass


class CookiecutterMainProxy(Proxy[str]):
    def request(self, *args, **kwargs) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        logger.info('Invocation cookiecutter.cli.main invocation: %s', json.dumps({
            'args': '[{arg_values}]'.format(arg_values=', '.join([f"'{str(x)}'" for x in args])),
            'kwargs': '{{{key_value_pairs}}}'.format(key_value_pairs=json.dumps({k: str(v) for k, v in kwargs.items()})),
        }))
        output_dir: str = super().request(*args, **kwargs)
        return output_dir


# Singleton and Adapter of Cookiecutter Proxy
class CookiecutterMainProxySingleton(metaclass=Singleton):

    def __init__(self) -> None:
        super().__init__()
        # wrapper around 'proxied' object; cookiecutter in this case
        cookiecutter_subject = CookiecutterMainSubject(cookiecutter_main)
        self._proxy = CookiecutterMainProxy(cookiecutter_subject)

    def __call__(self, *args: Any, **kwds: Any) -> str:
        return self._proxy.request(*args, **kwds)


cookiecutter_main = CookiecutterMainProxySingleton()
