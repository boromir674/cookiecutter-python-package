import typing as t

def parse_string(string: str) -> t.Dict: ...

class PoyoExceptionStub(Exception): ...

class ExceptionsAttribute(t.Protocol):
    PoyoException: t.Type[PoyoExceptionStub]

exceptions: ExceptionsAttribute
