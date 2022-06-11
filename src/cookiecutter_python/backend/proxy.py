import json
import logging
from typing import Generic, Mapping, TypeVar

from software_patterns import Proxy

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseProxy(Proxy[T], Generic[T]):
    @staticmethod
    def dumps(data_dict: Mapping, indent=4, sort_keys=True) -> str:
        return json.dumps(data_dict, indent=indent, sort_keys=sort_keys)
