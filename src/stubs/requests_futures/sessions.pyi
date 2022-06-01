from typing import Any

class Response:
    status_code: int

class Future:
    def result(self) -> Response: ...

class FuturesSession:
    def get(self, url: str, **kwargs: Any) -> Future: ...
