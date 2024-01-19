from abc import abstractmethod

from software_patterns import SubclassRegistry


class Dialog:
    @abstractmethod
    def dialog(self, *args, **kwargs):
        raise NotImplementedError


class DialogRegistry(SubclassRegistry[Dialog]):
    pass


class InteractiveDialog(metaclass=DialogRegistry):
    pass
