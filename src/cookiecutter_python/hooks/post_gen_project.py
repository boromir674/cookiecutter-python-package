#!/bin/env python3
"""
Cookiecutter post generation hook script that handles operations after the
template project is used to generate a target project.
"""
import os
import shlex
import subprocess
import sys
from collections import OrderedDict

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def get_templated_vars():
    # Templated Variables should be centralized here for easier inspection
    COOKIECUTTER = (
        OrderedDict()
    )  # We init the variable to the same type that will be set in the next line.
    COOKIECUTTER = {{ cookiecutter }}
    AUTHOR = "{{ cookiecutter.author }}"
    AUTHOR_EMAIL = "{{ cookiecutter.author_email }}"
    INITIALIZE_GIT_REPO_FLAG = "{{ cookiecutter.initialize_git_repo|lower }}"

    request = type('PostGenProjectRequest', (), {
        'cookiecutter': COOKIECUTTER,
        'project_dir': PROJECT_DIRECTORY,
        'author': AUTHOR,
        'author_email': AUTHOR_EMAIL,
        'initialize_git_repo': {'yes': True}.get(INITIALIZE_GIT_REPO_FLAG, False),
    })

    return request


def initialize_git_repo(project_dir: str):
    """
    Initialize the Git repository in the generated project.
    """
    subprocess.check_output("git init", stderr=subprocess.STDOUT, shell=True, cwd=project_dir)


def grant_basic_permissions(project_dir: str):
    try:
        subprocess.check_output(
            f"git config --global --add safe.directory {project_dir}",
            stderr=subprocess.STDOUT,
            shell=True,
            cwd=project_dir,
        )
    except Exception:
        print('WARNING')


def git_add(project_dir: str):
    """
    Do a Git add operation on the generated project.
    """
    subprocess.check_output(
        "git add --all", stderr=subprocess.STDOUT, shell=True, cwd=project_dir
    )


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

    env = os.environ.copy()
    env["GIT_COMMITTER_NAME"] = request.author
    env["GIT_COMMITTER_EMAIL"] = request.author_email

    request.author_info = f'{request.author} <{request.author_email}>'
    try:
        subprocess.check_output(
            (f'git commit --author "{request.author_info}"' f' --message "{commit_message}"'),
            shell=True,
            cwd=request.project_dir,
            env=env,
        )

    except subprocess.CalledProcessError as exc_info:
        if exc_info.returncode != 0:
            print(exc_info.output)
        raise


def python37_n_above_run_params(project_directory: str):
    return [shlex.split("git status --porcelain")], dict(
        capture_output=True,
        cwd=project_directory,
        check=True,
    )


def python36_n_below_run_params(project_directory: str):
    return (shlex.split("git status --porcelain"),), dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_directory,
        check=True,
    )


def _get_run_parameters(python3_minor: int):
    def run(args: list, kwargs: dict):
        return subprocess.run(*args, **kwargs)

    return {
        'legacy': lambda project_dir: run(*python36_n_below_run_params(project_dir)),
        # 'legacy': lambda project_dir: python36_n_below_run_params(project_dir),
        # 'new': lambda project_dir: python37_n_above_run_params(project_dir),
        'new': lambda project_dir: run(*python37_n_above_run_params(project_dir)),
    }[
        {True: 'legacy', False: 'new'}[
            python3_minor < 7  # is legacy Python 3.x version (ie 3.5 or 3.6) ?
        ]
    ]


def is_git_repo_clean(project_directory: str):
    """
    Check to confirm if the Git repository is clean and has no uncommitted
    changes. If its clean return True otherwise False.
    """

    try:
        git_status = _get_run_parameters(sys.version_info.minor)(project_directory)
    except subprocess.CalledProcessError as error:
        print(f"** Git repository in {project_directory} cannot get status")
        print('Exception: ' + str(error))
        raise error

    if git_status.stdout == b"" and git_status.stderr == b"":
        return True

    return False


def main(request):
    if request.initialize_git_repo:
        initialize_git_repo(request.project_dir)
        grant_basic_permissions(request.project_dir)
        if not is_git_repo_clean(request.project_dir):
            git_add(request.project_dir)
            git_commit(request)

    print("Finished Python Generation !!")
    sys.exit(0)


if __name__ == "__main__":
    REQUEST = get_templated_vars()
    main(REQUEST)
