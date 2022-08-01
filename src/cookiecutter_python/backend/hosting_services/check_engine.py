from typing import List, Tuple, Union

import attr

from .checker import Checker
from .handler import Handlers
from .web_hosting_service import HostingServices


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Engine:
    config_file: Union[None, str]
    default_config: Union[None, bool]
    services_info: Tuple

    checker: Checker = attr.ib(
        default=attr.Factory(
            lambda self: Checker.from_hosting_info(
                self.config_file, self.default_config, self.services_info
            ),
            takes_self=True,
        )
    )

    handlers: Handlers = attr.ib(
        default=attr.Factory(
            lambda self: Handlers.from_checkers(self.checker), takes_self=True
        )
    )

    def __getattr__(self, name):
        return getattr(self.checker, name)

    def handle(self, request_result):
        return self.handlers(request_result)

    def check(self, servers: List[str]):
        return iter(filter(None, [getattr(self, server)() for server in servers]))

    @staticmethod
    def create(config_file, default_config):
        return Engine(
            config_file,
            default_config,
            # load implementations and automatically instatiate all
            tuple((HostingServices.create(x) for x in ('pypi', 'readthedocs'))),
        )
