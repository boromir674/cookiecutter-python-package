from abc import ABC, abstractmethod
from typing import Optional, Generic, TypeVar

T = TypeVar('T')
O = TypeVar('O')


class Node(ABC, Generic[T, O]):

    @abstractmethod
    def process(self, request: T) -> Optional[O]:
        raise NotImplementedError
