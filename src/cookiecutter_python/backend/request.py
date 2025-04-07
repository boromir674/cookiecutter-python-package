import typing as t
from typing import Any, Iterable, List, Union

import attr

from .check_server_result import CheckWebServerResult


@attr.s(kw_only=True, auto_attribs=True, slots=True)
class Request:
    config_file: t.Union[str, None]
    default_config: bool
    web_servers: List[str]
    no_input: bool
    extra_context: t.Union[t.Dict, None]
    check: Any = attr.ib(default=None)
    check_results: Union[None, Iterable[CheckWebServerResult]] = attr.ib(default=None)
    offline: bool = False
