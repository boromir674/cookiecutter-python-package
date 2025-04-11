import typing as t

class Repo:
    def __init__(self, folder_path: str, **kwargs: t.Any) -> None: ...

class Actor:
    def __init__(self, name: str, email: str) -> None: ...
