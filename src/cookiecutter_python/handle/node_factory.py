from .dialogs import InteractiveDialog
from .node_base import DialogNode


class NodeFactory:
    @staticmethod
    def create(dialog_name: str):
        return DialogNode(
            InteractiveDialog.create(
                dialog_name,
            )
        )
