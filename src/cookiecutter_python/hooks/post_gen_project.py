#!/bin/env python3
"""
Cookiecutter post generation hook script that handles operations after the
template project is used to generate a target project.
"""
import os
import re
import subprocess
import sys
from collections import OrderedDict
from copy import copy
from os import path
from git import Actor, Repo

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def get_request():
    # Templated Variables should be centralized here for easier inspection
    COOKIECUTTER = (
        OrderedDict()
    )  # We init the variable to the same type that will be set in the next line.
    COOKIECUTTER = {{ cookiecutter }}  # pylint: disable=undefined-variable
    AUTHOR = "{{ cookiecutter.author }}"
    AUTHOR_EMAIL = "{{ cookiecutter.author_email }}"
    INITIALIZE_GIT_REPO_FLAG = "{{ cookiecutter.initialize_git_repo|lower }}"
    add_cli_flag = "{{ cookiecutter.add_cli|lower }}"

    request = type('PostGenProjectRequest', (), {
        'cookiecutter': COOKIECUTTER,
        'project_dir': PROJECT_DIRECTORY,
        'module_name': COOKIECUTTER['pkg_name'],
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'initialize_git_repo': {'yes': True}.get(INITIALIZE_GIT_REPO_FLAG, False),
        'add_cli': {'yes': True}.get(add_cli_flag, False),
        'repo': None,
    })

    return request


class PostFileRemovalError(Exception):
    pass

def post_file_removal(request):
    files_to_remove = []
    if not request.add_cli:
        files_to_remove.extend([
            path.join(request.project_dir, 'src', request.module_name, 'cli.py'),
            path.join(request.project_dir, 'src', request.module_name, '__main__.py'),
        ])
    for file in files_to_remove:
        os.remove(file)


def _get_run_parameters(python3_minor: int):
    def run(args: list, kwargs: dict):
        return subprocess.run(*args, **kwargs)
    def _subprocess_run(get_params):
        def run1(*args, **kwargs):
            return run(*get_params(*args, **kwargs))
        return run1

    return {
        'legacy': _subprocess_run(run_process_python36_n_below),
        'new': _subprocess_run(run_process_python37_n_above),
    }[
        {True: 'legacy', False: 'new'}[
            python3_minor < 7  # is legacy Python 3.x version (ie 3.5 or 3.6) ?
        ]
    ]


def run_process_python37_n_above(*args, **kwargs):
    return [args], dict(capture_output=True, check=True, **kwargs)

def run_process_python36_n_below(*args, **kwargs):
    return [args], dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, **kwargs)


def subprocess_run(*args, **kwargs):
    return _get_run_parameters(sys.version_info.minor)(*args, **kwargs)


def initialize_git_repo(project_dir: str):
    """
    Initialize the Git repository in the generated project.
    """
    subprocess_run('git', 'init', cwd=project_dir)


def exception(subprocess_exception: subprocess.CalledProcessError):
    if re.match(r'error: could not lock config file .+\.gitconfig File exists',
        error := str(subprocess_exception.stderr, encoding='utf-8')):
        return type('LockFileError', (Exception,), {})(error)
    return subprocess_exception

def grant_basic_permissions(project_dir: str):
    try:
        return subprocess_run(
            'git', 'config', '--global', '--add', 'safe.directory', project_dir,
            cwd=project_dir,
        )
    except subprocess.CalledProcessError as error:
        print('Did not add an entry in ~/.gitconfig!')
        print(str(error.stderr, encoding='utf-8'))
        print(exception(error))


def git_commit(request):
    """Commit the staged changes in the generated project."""
    cookiecutter_config_str = (
        '\n'.join((f"  {key}: {val}" for key, val in request.cookiecutter.items())) + '\n'
    )
    commit_message = (
        "Template applied from"
        " https://github.com/boromir674/cookiecutter-python-"
        "package\n\n"
        "Template configuration:\n"
        f"{cookiecutter_config_str}"
    )
    request.repo.index.add(os.listdir(request.project_dir))
    author = Actor(request.author, request.author_email)

    request.repo.index.commit(
        commit_message,
        author=author,
        committer=copy(author)
    )


def is_git_repo_clean(project_directory: str):
    """
    Check to confirm if the Git repository is clean and has no uncommitted
    changes. If its clean return True otherwise False.
    """
    try:
        git_status = subprocess_run('git', 'status', '--porcelain', cwd=project_directory)
    except subprocess.CalledProcessError as error:
        print(f"** Git repository in {project_directory} cannot get status")
        print('Exception: ' + str(error))
        raise error

    if git_status.stdout == b"" and git_status.stderr == b"":
        return True

    return False


def _post_hook():
    print('\n --- POST GEN SCRIPT')
    request = get_request()
    post_file_removal(request)
    if request.initialize_git_repo:
        try:
            initialize_git_repo(request.project_dir)
            grant_basic_permissions(request.project_dir)
            request.repo = Repo(request.project_dir)
            if not is_git_repo_clean(request.project_dir):
            # if request.repo.index.diff(None):  # there are changes not added to index
                git_commit(request)
            else:
                print('Index did not update !!')
        except Exception as error:
            print(f"{error}\nERROR in Post Script.\nExiting with 1")
            return 1
    return 0


def post_hook():
    sys.exit(_post_hook())


def main():
    post_hook()


if __name__ == "__main__":
    main()
