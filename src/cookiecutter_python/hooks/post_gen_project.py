"""Post Cookie Hook: Templated File with jinja2 syntax

Cookiecutter post generation hook script that handles operations after the
template project is used to generate a target project.
"""
#!/usr/bin/env python3

import shutil
import os
import re
import subprocess
import sys
import typing as t
from collections import OrderedDict
from copy import copy
from os import path
from pathlib import Path
from git import Actor, Repo
from cookiecutter_python.backend.gen_docs_common import get_docs_gen_internal_config

import logging

logger = logging.getLogger(__name__)

# Path to dir, where the a newly Scaffolded Project is generated in
# ie: if we scaffold new Project at /data/my-project/README.md, /data/my-project/src
# then GEN_PROJ_LOC = /data/my-project
GEN_PROJ_LOC = os.path.realpath(os.path.curdir)

# Doc Builders docs default location, after Generation
DOCS: t.Dict[str, str] = get_docs_gen_internal_config()

def get_context() -> OrderedDict:
    """Get the Context, that was used by the Templating Engine at render time"""
    # variable with an object of the same type that will be set in the next line
    COOKIECUTTER: OrderedDict = OrderedDict()
    COOKIECUTTER = {{ cookiecutter }}  # type: ignore    # pylint: disable=undefined-variable
    return COOKIECUTTER


def get_request():
    cookie_dict: OrderedDict = get_context()
    INITIALIZE_GIT_REPO_FLAG = "{{ cookiecutter.initialize_git_repo|lower }}"

    # DATA: str to value mapping
    data: t.Dict[str, t.Any] = {
        'cookiecutter': cookie_dict,
        'project_dir': GEN_PROJ_LOC,
        'module_name': cookie_dict['pkg_name'],
        'author': "{{ cookiecutter.author }}",
        'author_email': "{{ cookiecutter.author_email }}",
        'initialize_git_repo': {'yes': True}.get(INITIALIZE_GIT_REPO_FLAG, False),
        'project_type': "{{ cookiecutter.project_type }}",
        # 'add_cli': {'module+cli': True}.get(project_type, False),
        'repo': None,
        # Docs Website: build/infra config, and Content Templates
        'docs_website': {
            'builder': cookie_dict['docs_builder'],
            'python_runtime': cookie_dict['rtd_python_version'],
        },
        'docs_extra_info': DOCS,
    }
    # sanity check on data dict for docs_website and docs_extra_info
    # TODO: remove sanity checks
    assert 'docs_website' in data.keys(), f"ERROR 1: 'docs_website' not in data.keys()={data.keys()}"
    assert 'builder' in data['docs_website'].keys(), f"ERROR 2: 'builder' not in data['docs_website'].keys()={data['docs_website'].keys()}"
    assert 'docs_extra_info' in data.keys(), f"ERROR 3a: 'docs_extra_info' not in data.keys()={data.keys()}"
    assert data['docs_website']['builder'] in {'mkdocs', 'sphinx'}, f"ERROR 3b: docs_website.builder={data['docs_website']['builder']} not in ['mkdocs', 'sphinx']"

    from pprint import pprint
    pprint("\n\n")
    pprint(data)
    assert data['docs_website']['builder'] in data['docs_extra_info'].keys(), f"ERROR 3: docs_website.builder={data['docs_website']['builder']} not in docs_extra_info.keys()={data['docs_extra_info'].keys()}"
    request = type('PostGenProjectRequest', (), data)
    assert hasattr(request, 'docs_extra_info')
    assert hasattr(request, 'docs_website')
    return request


class PostFileRemovalError(Exception):
    pass

### Define specialized files present per 'project_type' ###
# (ie 'module' or 'module+cli')
# each set of files exists exclusively for a given 'project_type'

# CLI have extra files for command-line entrypoint and unit testing them
CLI_ONLY = lambda x: [
    ('src', x.module_name, 'cli.py'),
    ('src', x.module_name, '__main__.py'),
    ('tests', 'test_cli.py'),
    ('tests', 'test_invoking_cli.py'),
]
# Pytest plugin must use the legacy setuptools backend (no poetry)
# thus the setup.cfg and MANIFEST.in files are required
# Pytest pluging usually declare their public API in fixtures.py
PYTEST_PLUGIN_ONLY = lambda x: [
    ('src', x.module_name, 'fixtures.py'),
    ('tests', 'conftest.py'),
    ('tests', 'test_my_fixture.py'),
    ('setup.cfg',),
    ('MANIFEST.in',),
]
# Specify the files to be deleted, in post-process, for each project type
delete_files = {
    'pytest-plugin': lambda x: CLI_ONLY(x),
    'module': lambda x: CLI_ONLY(x) + PYTEST_PLUGIN_ONLY(x),
    'module+cli': lambda x: PYTEST_PLUGIN_ONLY(x),
}

# TODO: read from cookiecuuter['_template'] / cookiecutter.json
# delete mkdocs.yml if not using mkdocs
# delete sphinx files if not using sphinx
builder_id_2_files = {
    'mkdocs': ['mkdocs.yml'],
}

def post_file_removal(request):
    """Preserve only files relevant to Project Type requested to Generate.

    Delete files that are not relevant to the project type requested to
    generate.
    
    For example, if the user requested a 'module' project type,
    then delete the files that are only relevant to a 'module+cli' project.

    Args:
        request ([type]): [description]
    """
    from pathlib import Path
    
    files_to_remove = [
        os.path.join(request.project_dir, *x) for x in delete_files[request.project_type](request)
    ]
    ## Post Removal, given 'Project Type', of potentially extra files ##
    for file in files_to_remove:
        os.remove(file)

    ## Remove gen 'docs' folders, given 'Docs Website Builder' (DWB) ##
    for builder_id, gen_docs_folder_name in request.docs_extra_info.items():
        if builder_id != request.docs_website['builder']:
            shutil.rmtree(str(Path(request.project_dir) / gen_docs_folder_name))
    
    ## Remove top level files (ie mkdocs.yml), defined in builder_id_2_files map ##
    for builder_id, files in builder_id_2_files.items():
        if builder_id != request.docs_website['builder']:
            for file in files:
                os.remove(os.path.join(request.project_dir, file))


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


def is_git_repo_clean(project_directory: str) -> bool:
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
    """Delete irrelevant to Project Type files and optionally do git commit."""
    request = get_request()
    # Delete gen Files related to
    #  - different Project Type
    #  - related to different documentation builder tool"""
    post_file_removal(request)
    # move/rename docs-builder-specific docs folder to 'docs/'
    try:
        os.rename(
            str(Path(request.project_dir) / request.docs_extra_info[request.docs_website['builder']]),
            os.path.join(request.project_dir, 'docs')
        )
    except OSError as error:
        print(f"** Could not move/rename '{request.docs_extra_info[request.docs_website['builder']]}' to 'docs/'")
        print('Exception: ' + str(error))
        raise error

    # Git commit
    if request.initialize_git_repo:
        initialize_git_repo(request.project_dir)
        # grant_basic_permissions(request.project_dir)
        request.repo = Repo(request.project_dir)
        if not is_git_repo_clean(request.project_dir):
            git_commit(request)
        else:
            print('No changes to commit.')
    return 0


def post_hook():
    """Delete irrelevant to Project Type files and optionally do git commit."""
    sys.exit(_post_hook())


def main():
    """Delete irrelevant to Project Type files and optionally do git commit."""
    post_hook()


if __name__ == "__main__":
    main()
