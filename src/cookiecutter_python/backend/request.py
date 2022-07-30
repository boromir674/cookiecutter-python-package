from typing import Any, Iterable, List, Protocol, Union

import attr


class CheckResult(Protocol):
    service_name: str
    name: str


@attr.s(kw_only=True, auto_attribs=True, slots=True)
class Request:
    config_file: str
    default_config: bool
    web_servers: List[str]
    no_input: bool
    extra_context: dict
    check: Any = attr.ib(default=None)
    check_results: Union[None, Iterable[CheckResult]] = attr.ib(default=None)
