from typing import Callable, Protocol, Tuple, Union

import attr

from .checkers import Checkers


class FutureResult(Protocol):
    status_code: int


class Future(Protocol):
    def result(self) -> FutureResult:
        ...


ServiceChecker = Callable[[Union[None, str], Union[None, str]], Tuple[Future, str]]


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Checker:
    config_file: Union[None, str]
    default_config: Union[None, bool]
    checkers: Checkers

    def __getattr__(self, service_name: str) -> ServiceChecker:
        return self.checkers[service_name]

    def __iter__(self):
        return iter(self.checkers)

    @staticmethod
    def from_hosting_info(config_file, default_config, hosting_infos):
        return Checker(
            config_file,
            default_config,
            Checkers.from_hosting_info(
                hosting_infos, config_file and not default_config, config_file
            ),
        )
