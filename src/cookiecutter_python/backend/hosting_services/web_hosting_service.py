import attr
from software_patterns import SubclassRegistry


@attr.s(auto_attribs=True, slots=True, frozen=True)
class URLGetter:
    url_pattern: str
    service_name: str

    def __call__(self, name: str):
        return self.url_pattern.format(name=name)

    def __str__(self):
        return self.service_name


@attr.s(auto_attribs=True, slots=True, frozen=True)
class WebHostingService:
    url: URLGetter

    def __str__(self):
        return str(self.url)

    @staticmethod
    def create(url_pattern: str, service_name: str):
        return WebHostingService(URLGetter(url_pattern, service_name))


class HostingServiceInfo:
    def create(self, *args, **kwargs):
        """Factory method for creating WebHostingService instances.

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError

    @property
    def service(self):
        return self.create()

    @property
    def variable_name(self) -> str:
        raise NotImplementedError


class HostingServicesInfo(SubclassRegistry[HostingServiceInfo]):
    pass


class HostingServices(metaclass=HostingServicesInfo):
    pass


@HostingServices.register_as_subclass('pypi')
class PyPIServerFactory(HostingServiceInfo):
    def create(self, *args, **kwargs):
        return WebHostingService.create('https://pypi.org/project/{name}', 'pypi')

    @property
    def variable_name(self) -> str:
        return 'pkg_name'


@HostingServices.register_as_subclass('readthedocs')
class ReadTheDocsServerFactory(HostingServiceInfo):
    def create(self, *args, **kwargs):
        return WebHostingService.create('https://{name}.readthedocs.io/', 'readthedocs')

    @property
    def variable_name(self) -> str:
        return 'readthedocs_project_slug'
