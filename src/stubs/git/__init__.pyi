import os
import typing as t


class Repo:
    def __init__(self, folder_path: str, **kwargs: t.Any) -> None: ...

    @classmethod
    def init(
        cls,
        path: t.Union[t.Union[str, "os.PathLike[str]"], None] = None,
        mkdir: bool = True,
        # odbt: t.Type[GitCmdObjectDB] = GitCmdObjectDB,
        expand_vars: bool = True,
        **kwargs: t.Any,
    ) -> "Repo": ...
    
    def is_dirty(self, **kwargs: t.Any) -> bool: ...
    
    @property
    def git(self) -> t.Any: ...


class Actor:
    def __init__(self, name: str, email: str) -> None: ...
