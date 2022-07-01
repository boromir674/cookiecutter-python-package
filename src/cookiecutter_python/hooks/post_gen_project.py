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
from pathlib import Path

from git import Actor, Repo

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def get_request():
    # We init the variable to the same type that will be set in the next line.
    COOKIECUTTER = OrderedDict()
    COOKIECUTTER = {{ cookiecutter }}  # pylint: disable=undefined-variable
    INITIALIZE_GIT_REPO_FLAG = "{{ cookiecutter.initialize_git_repo|lower }}"

    request = type('PostGenProjectRequest', (), {
        'cookiecutter': COOKIECUTTER,
        'project_dir': PROJECT_DIRECTORY,
        'module_name': COOKIECUTTER['pkg_name'],
        'author': "{{ cookiecutter.author }}",
        'author_email': "{{ cookiecutter.author_email }}",
        'initialize_git_repo': {'yes': True}.get(INITIALIZE_GIT_REPO_FLAG, False),
        'project_type': "{{ cookiecutter.project_type }}",
        # 'add_cli': {'module+cli': True}.get(project_type, False),
        'repo': None,
    })
    return request


class PostFileRemovalError(Exception):
    pass


CLI_ONLY = lambda x: [
    ('src', x.module_name, 'cli.py'),
    ('src', x.module_name, '__main__.py'),
    ('tests', 'test_cli.py'),
    ('tests', 'test_invoking_cli.py'),
]
PYTEST_PLUGIN_ONLY = lambda x: [
    ('tests', 'conftest.py'),
    ('tests', 'test_my_fixture.py'),
    ('setup.cfg',),
    ('MANIFEST.in',),
]
delete_files = {
    'pytest-plugin': lambda x: CLI_ONLY(x),
    'module': lambda x: CLI_ONLY(x) + PYTEST_PLUGIN_ONLY(x),
    'module+cli': lambda x: PYTEST_PLUGIN_ONLY(x),
}

def post_file_removal(request):
    print(request.project_type)
    files_to_remove = [
        path.join(request.project_dir, *x) for x in delete_files[request.project_type](request)
    ]
    for file in files_to_remove:
        os.remove(file)


def _get_run_parameters(python3_minor: int):
    def run(args: list, kwargs: dict):
        return subprocess.run(*args, **dict(kwargs, check=True)) # pylint: disable=W1510 #nosec
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
    error_message = str(subprocess_exception.stderr, encoding='utf-8')
    if re.match(r'error: could not lock config file .+\.gitconfig File exists',
        error_message):
        return type('LockFileError', (Exception,), {})(error_message)
    return subprocess_exception

def grant_basic_permissions(project_dir: str):
    try:
        return subprocess_run(
            'git', 'config', '--global', '--add', 'safe.directory', str(project_dir),
            cwd=project_dir,
        )
    except subprocess.CalledProcessError as error:
        print('Did not add an entry in ~/.gitconfig!')
        print(str(error.stderr, encoding='utf-8'))
        print(exception(error))


def iter_files(request):
    path_obj = Path(request.project_dir)
    for file_path in path_obj.rglob('*'):
        if bool(
            path.isfile(file_path) and
            '__pycache__' not in str(file_path) and
            str(os.path.relpath(file_path, start=request.project_dir)) != '.git' and
            not str(os.path.relpath(file_path, start=request.project_dir)).startswith('.git/')
        ):
            yield str(file_path)


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

    request.repo.index.add(list(
        iter((path.relpath(x, start=request.project_dir) for x in iter_files(request)))
    ))
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
        initialize_git_repo(request.project_dir)
        grant_basic_permissions(request.project_dir)
        request.repo = Repo(request.project_dir)
        if not is_git_repo_clean(request.project_dir):
            git_commit(request)
        else:
            print('Index did not update !!')
    return 0


def post_hook():
    sys.exit(_post_hook())


def main():
    post_hook()


if __name__ == "__main__":
    main()
