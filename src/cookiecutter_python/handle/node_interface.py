from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar


T = TypeVar('T')
TT = TypeVar('TT')


class Node(ABC, Generic[T, TT]):
    @abstractmethod
    def process(self, request: T) -> Optional[TT]:
        raise NotImplementedError
