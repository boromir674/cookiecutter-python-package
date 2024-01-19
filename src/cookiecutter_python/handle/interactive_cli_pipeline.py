"""Handles sequence of Interactive User Dialogs, for Context Information."""

from .node_factory import NodeFactory


class InteractiveDialogsPipeline:
    """Handles sequence of Interactive User Dialogs, for Context Information."""

    dialogs = [
        'project-name',
        # 'project_type',
        # 'project_slug',
        # 'pkg_name',
        # 'repo_name',
        # 'readthedocs_project_slug',
        # 'docker_image',
        # 'full_name',
        # 'author',
        # 'author_email',
        # 'github_username',
        # 'project_short_description',
        # 'pypi_subtitle',
        # 'release_date',
        # 'year',
        # 'version',
        # 'initialize_git_repo',
        # 'interpreters',
        # 'docs_builder',
        # 'rtd_python_version',
    ]

    def process(self, request):
        """Process sequence of Interactive User Dialogs, for Context Information."""
        for dialog in self.dialogs:
            request = NodeFactory.create(dialog).process(request)
        return request
