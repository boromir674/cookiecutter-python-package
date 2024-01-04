from typing import Mapping, Optional
from questionary import prompt
from ..dialog import InteractiveDialog

import datetime

@InteractiveDialog.register_as_subclass('project-name')
class ProjectNameDialog:

    def dialog(
        self,
        project_types,
        full_name,
        ci_matrix_interpreters,
        default: Optional[str]) -> Mapping[str, str]:
        return prompt(
            [
                {
                    'type': 'input',
                    'name': 'project_name',
                    'message': 'Enter the Project Name (ie human-readable text):',
                    'default': default or None,
                },
                {
                    'type': 'select',
                    'name': 'project_type',
                    'message': 'Select the Project Type:',
                    'choices': project_types,
                    'default': project_types[0],
                },
                {
                    'type': 'input',
                    'name': 'project_slug',
                    'message': 'Enter the Project Slug (ie lowercase text, no spaces):',
                    'default': lambda answers: answers['project_name'].lower().replace(' ', '-'),
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
                    'default': full_name or 'Your Name',
                },
                # author_email
                {
                    'type': 'input',
                    'name': 'author_email',
                    'message': 'Enter author_email:',
                    'default': lambda answers: answers['full_name'].replace(' ', '.').lower() + '@example.com',
                },
                # github_username
                {
                    'type': 'input',
                    'name': 'github_username',
                    'message': 'Enter github_username:',
                    # 'default': None,
                },
                # project_short_description
                {
                    'type': 'input',
                    'name': 'project_short_description',
                    'message': 'Enter project_short_description:',
                    # 'default': None,
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
                    'default': '0.0.1',
                },
                # initialize_git_repo
                {
                    'type': 'select',
                    'name': 'initialize_git_repo',
                    'message': 'Initialize Git Repository?',
                    'choices': ['yes', 'no'],
                    'default': 'yes',
                },
                # interpreters
                {
                    'type': 'checkbox',
                    'name': 'supported-interpreters',
                    'message': 'Select the python Interpreters you wish to support',
                    'choices': ci_matrix_interpreters,
                    # 'default': ['3.6', '3.7', '3.8', '3.9', '3.10', '3.11'],
                },
                # docs_builder
                {
                    'type': 'select',
                    'name': 'docs_builder',
                    'message': 'Select the docs builder you wish to use',
                    'choices': ['sphinx', 'mkdocs'],
                    'default': 'sphinx',
                },
                # rtd_python_version
                {
                    'type': 'select',
                    'name': 'rtd_python_version',
                    'message': 'Select the python version you wish to use for ReadTheDocs',
                    'choices': ['3.8', '3.9', '3.10', '3.11', '3.12'],
                    'default': '3.8',
                },
            ]
        )
