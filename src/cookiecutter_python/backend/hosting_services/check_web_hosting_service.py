from typing import Callable

import attr
from requests_futures.sessions import FuturesSession


@attr.s(auto_attribs=True, slots=True, frozen=True)
class WebHostingServiceChecker:
    url_getter: Callable[[str], str]

    def __call__(self, name: str):
        session = FuturesSession()
        future = session.get(self.url_getter(name))
        return type(
            'RequestResult',
            (),
            {'future': future, 'name': name, 'service_name': str(self.url_getter)},
        )

    def __str__(self):
        return str(self.url_getter)

    @staticmethod
    def create(hosting_service):
        return WebHostingServiceChecker(hosting_service.url)
