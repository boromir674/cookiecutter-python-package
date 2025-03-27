import datetime
from typing import Mapping

from questionary import Choice, prompt

from ..dialog import InteractiveDialog


@InteractiveDialog.register_as_subclass('project-name')
class ProjectNameDialog:
    def dialog(self, cookie_vars) -> Mapping[str, str]:
        # TODO: automatically create list from cookiecutter json
        return prompt(
            [
                {
                    'type': 'input',
                    'name': 'project_name',
                    'message': 'Enter the Project Name (ie human-readable text):',
                    'default': cookie_vars['project_name'],
                },
                {
                    'type': 'select',
                    'name': 'project_type',
                    'message': 'Select the Project Type:',
                    'choices': cookie_vars['project_type']['choices'],
                    'default': cookie_vars['project_type']['default'],
                },
                {
                    'type': 'input',
                    'name': 'project_slug',
                    'message': 'Enter the Project Slug (ie lowercase text, no spaces):',
                    'default': lambda answers: answers['project_name']
                    .lower()
                    .replace(' ', '-'),
                },
                {
                    'type': 'input',
                    'name': 'pkg_name',
                    'message': 'Enter the Package Name (ie lowercase text, no spaces):',
                    'default': lambda answers: answers['project_slug'].replace('-', '_'),
                },
                {
                    'type': 'input',
                    'name': 'repo_name',
                    'message': 'Enter the Repository Name (ie lowercase text, no spaces):',
                    'default': lambda answers: answers['project_slug'],
                },
                {
                    'type': 'input',
                    'name': 'readthedocs_project_slug',
                    'message': 'Enter the ReadTheDocs Project Slug (ie lowercase text, no spaces):',
                    'default': lambda answers: answers['project_slug'],
                },
                {
                    'type': 'input',
                    'name': 'docker_image',
                    'message': 'Enter the Docker Image Name (ie lowercase text, no spaces):',
                    'default': lambda answers: answers['project_slug'],
                },
                # full_name
                {
                    'type': 'input',
                    'name': 'full_name',
                    'message': 'Enter full_name:',
                    'default': cookie_vars['full_name'],
                },
                # author
                {
                    'type': 'input',
                    'name': 'author',
                    'message': 'Enter author:',
                    'default': lambda answers: answers['full_name'],
                },
                # author_email
                {
                    'type': 'input',
                    'name': 'author_email',
                    'message': 'Enter author_email:',
                    'default': cookie_vars['author_email'],
                },
                # github_username
                {
                    'type': 'input',
                    'name': 'github_username',
                    'message': 'Enter github_username:',
                    'default': cookie_vars['github_username'],
                },
                # project_short_description
                {
                    'type': 'input',
                    'name': 'project_short_description',
                    'message': 'Enter project_short_description:',
                    'default': cookie_vars['project_short_description'],
                },
                # pypi_subtitle
                {
                    'type': 'input',
                    'name': 'pypi_subtitle',
                    'message': 'Enter pypi_subtitle:',
                    'default': lambda answers: answers['project_short_description'],
                },
                # release_date
                {
                    'type': 'input',
                    'name': 'release_date',
                    'message': 'Enter release_date:',
                    # Default is NOW
                    'default': datetime.datetime.now().strftime('%Y-%m-%d'),
                },
                # year
                {
                    'type': 'input',
                    'name': 'year',
                    'message': 'Enter year:',
                    # Default is NOW
                    'default': datetime.datetime.now().strftime('%Y'),
                },
                # version
                {
                    'type': 'input',
                    'name': 'version',
                    'message': 'Enter version:',
                    'default': cookie_vars['version'],
                },
                # initialize_git_repo
                {
                    'type': 'select',
                    'name': 'initialize_git_repo',
                    'message': 'Initialize Git Repository?',
                    'choices': cookie_vars['initialize_git_repo']['choices'],
                    'default': cookie_vars['initialize_git_repo']['default'],
                },
                # interpreters
                {
                    'type': 'checkbox',
                    'name': 'supported-interpreters',
                    'message': 'Select the python Interpreters you wish to support',
                    'choices': [
                        Choice(str(x[0]), checked=bool(x[1]))
                        for x in cookie_vars['supported-interpreters']['choices']
                    ],
                    # 'default': ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11'],
                },
                # docs_builder
                {
                    'type': 'select',
                    'name': 'docs_builder',
                    'message': 'Select the docs builder you wish to use',
                    'choices': cookie_vars['docs_builder']['choices'],
                    'default': cookie_vars['docs_builder']['default'],
                },
                # rtd_python_version
                {
                    'type': 'select',
                    'name': 'rtd_python_version',
                    'message': 'Select the python version you wish to use for ReadTheDocs',
                    # 'choices': ['3.8', '3.9', '3.10', '3.11', '3.12'],
                    'choices': cookie_vars['rtd_python_version']['choices'],
                    'default': cookie_vars['rtd_python_version']['default'],
                },
                # CICD Pipeline design: stable, experimental
                {
                    'type': 'select',
                    'name': 'cicd',
                    'message': 'Select the CI/CD Pipeline Design',
                    'choices': cookie_vars['cicd']['choices'],
                    'default': cookie_vars['cicd']['default'],
                },
            ]
        )
