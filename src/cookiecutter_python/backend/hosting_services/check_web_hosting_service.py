from typing import Protocol

import attr
from requests_futures.sessions import FuturesSession


class WebHostingService(Protocol):
    def url(self, name: str) -> str:
        ...


@attr.s(auto_attribs=True, slots=True, frozen=True)
class WebHostingServiceChecker:
    hosting_service: WebHostingService

    def __call__(self, name: str):
        session = FuturesSession()
        future = session.get(self.hosting_service.url(name))
        return type(
            'RequestResult',
            (),
            {'future': future, 'name': name, 'service_name': str(self.hosting_service)},
        )

    def __str__(self):
        return str(self.hosting_service)
