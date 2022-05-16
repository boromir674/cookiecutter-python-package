from typing import Any, Protocol

class Response(Protocol):
    status_code: int

class Future(Protocol):
    def result(self) -> Response: ...

class FuturesSession(Protocol):
    def get(self, url: str, **kwargs: Any) -> Future: ...
