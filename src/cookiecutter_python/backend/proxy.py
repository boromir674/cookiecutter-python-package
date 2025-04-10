import json
import logging
from typing import Generic, Tuple, TypeVar

from software_patterns import Proxy


logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseProxy(Proxy[T], Generic[T]):
    @staticmethod
    def log_info_args(message: str, *args, **kwargs) -> Tuple[str, str]:
        return message, json.dumps(
            {
                'keyword_args': {k: str(v) for k, v in kwargs.items()},
                'positional_args': [str(arg_value) for arg_value in args],
            },
            indent=4,
            sort_keys=True,
        )
