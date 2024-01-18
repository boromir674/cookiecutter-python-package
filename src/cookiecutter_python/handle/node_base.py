import typing as t

from .node_interface import Node


class DialogNode(Node[t.List, t.Mapping[str, t.Any]]):
    """Handles a single Interactive User Dialog, for Context Information."""

    def __init__(self, dialog):
        self.ela = dialog

    def process(self, request):
        """Process a single Interactive User Dialog, for Context Information."""
        return self.ela.dialog(*request)
