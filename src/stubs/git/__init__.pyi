from typing import Protocol, List, Optional


class Actor(Protocol):
    name: str
    email: str


class Commit(Protocol):
    type: str
    message: str
    author: Actor


class IndexLike(Protocol):
    def add(self, files_list: List[str]): ...

    def commit(self,
        commit_message: str,
        author: Optional[Actor] = None,
        committer: Optional[Actor] = None
    ): ...


class Repo:
    def __init__(self, repo_path: str): ...

    def commit(self, reference: str) -> Commit: ...

    @property
    def index(self) -> IndexLike: ...
