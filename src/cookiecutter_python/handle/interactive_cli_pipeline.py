"""Handles sequence of Interactive User Dialogs, for Context Information."""

from .node_factory import NodeFactory


class InteractiveDialogsPipeline:
    """Handles sequence of Interactive User Dialogs, for Context Information."""

    dialogs = [
        'project-name',
    ]

    def process(self, request):
        """Process sequence of Interactive User Dialogs, for Context Information."""
        for dialog in self.dialogs:
            request = NodeFactory.create(dialog).process(request)
        return request
