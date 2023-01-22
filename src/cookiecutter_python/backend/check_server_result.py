from abc import ABC, abstractmethod


class CheckWebServerResult(ABC):
    """Interface for checking the result of a web server request."""

    @property
    @abstractmethod
    def future(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the resource requested to search on the web server.

        Returns:
            str: the name of the resource (ie python package slug, rtd project)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def service_name(self) -> str:
        """The name of the web server.

        Returns:
            str: the name (slug) of the web server
        """
        raise NotImplementedError
