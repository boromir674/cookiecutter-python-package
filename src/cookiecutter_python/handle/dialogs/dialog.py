from abc import abstractmethod

from software_patterns import SubclassRegistry


class InteractiveDialog(metaclass=SubclassRegistry):
    @abstractmethod
    def dialog(self, *args, **kwargs):
        raise NotImplementedError
