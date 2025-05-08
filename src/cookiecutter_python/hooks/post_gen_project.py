"""Post Cookie Hook: Templated File with jinja2 syntax

Cookiecutter post generation hook script that handles operations after the
template project is used to generate a target project.
"""
#!/usr/bin/env python3

import json
import os
import shutil
import sys
import typing as t
from collections import OrderedDict
from copy import copy
from os import path
from pathlib import Path


try:
    from git import Actor, Repo
except ImportError:  # git binary not found
    git_binary_found = False
else:
    git_binary_found = True

import logging

from cookiecutter_python._logging_config import FILE_TARGET_LOGS


logger = logging.getLogger(__name__)

# Path to dir, where the a newly Scaffolded Project is generated in
# ie: if we scaffold new Project at /data/my-project/README.md, /data/my-project/src
# then GEN_PROJ_LOC = /data/my-project
GEN_PROJ_LOC = os.path.realpath(os.path.curdir)

# Doc Builders docs default location, after Generation
# DOCS: t.Dict[str, str] = get_docs_gen_internal_config()


def get_context() -> OrderedDict:
    """Get the Context, that was used by the Templating Engine at render time"""
    # variable with an object of the same type that will be set in the next line
    COOKIECUTTER: OrderedDict = OrderedDict()
    COOKIECUTTER = {{cookiecutter}}  # type: ignore    # pylint: disable=undefined-variable  # noqa: F821
    return COOKIECUTTER


def get_request():
    cookie_dict: OrderedDict = get_context()

    data: t.Dict[str, t.Any] = {
        'vars': cookie_dict,
        'project_dir': GEN_PROJ_LOC,
        'module_name': cookie_dict['pkg_name'],
        'initialize_git_repo': {'yes': True}.get(
            cookie_dict['initialize_git_repo'].lower(), False
        ),
        'repo': None,
        # Docs Website: build/infra config, and Content Templates
        'docs_website': {
            'builder': cookie_dict['docs_builder'],
            'python_runtime': cookie_dict['rtd_python_version'],
        },
    }
    return type('PostGenProjectRequest', (), data)


### Define specialized files present per 'project_type' ###
# each set of files exists exclusively for a given 'project_type'


# CLI have extra files for command-line entrypoint and unit testing them
def CLI_ONLY(x):
    return [
        ('src', x.module_name, 'cli.py'),
        ('src', x.module_name, '__main__.py'),
        ('tests', 'test_cli.py'),
        ('tests', 'test_invoking_cli.py'),
    ]


# Pytest plugin must use the legacy setuptools backend (no poetry)
# thus the setup.cfg and MANIFEST.in files are required
# Pytest pluging usually declare their public API in fixtures.py
def PYTEST_PLUGIN_ONLY(x):
    return [
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

### Define specialized files present per 'CI/CD option' ###
CICD_DELETE: t.Dict[str, t.List[t.Tuple[str, ...]]] = {
    'stable': [
        ('.github', 'workflows', 'cicd.yml'),
        ('.github', 'workflows', 'codecov-upload.yml'),
        ('.github', 'workflows', 'signal-deploy.yml'),
    ],
    'experimental': [
        ('.github', 'workflows', 'test.yaml'),
    ],
}
### Define specialized files present per 'Docs Builder' option ###
DOCS_FILES_EXTRA = {
    'mkdocs': ['mkdocs.yml', 'scripts/gen_api_refs_pages.py'],
}


###### POST Gen FILE REMOVALs
def post_file_removal(request):
    """Preserve only files relevant to Project Type requested to Generate."""
    # Remove files that are not relevant to the selected project type {module, cli+comule, pytest-plugin}
    files_to_remove = [
        os.path.join(request.project_dir, *x)
        for x in delete_files[request.vars['project_type']](request)
    ]
    _delete_files(files_to_remove)
    # Remove files that are not relevant to the selected CI/CD Design option
    irrelevant_ci_cd_files = [
        os.path.join(request.project_dir, *path_components)
        for path_components in CICD_DELETE[request.vars['cicd']]
    ]
    _delete_files(irrelevant_ci_cd_files)
    # Remove generated docs folders, but the input builder (ie mkdocs/sphinx) selected
    _remove_irrelevant_docs_folders(request.project_dir)
    # Remove some top-level files depending on input (ie mkdocs.yml)
    _remove_irrelevant_top_level_files(request)


def _remove_irrelevant_docs_folders(gen_project_dir: str):
    """Remove generated docs folders that are not relevant to the selected docs builder."""
    # find top-level folders and delte the ones with name 'PyGen_TO_DELETE'
    for docs_folder_to_delete in (
        folder
        for folder in Path(gen_project_dir).iterdir()
        if folder.is_dir() and folder.name == 'PyGen_TO_DELETE'
    ):
        shutil.rmtree(docs_folder_to_delete, ignore_errors=True)


def _remove_irrelevant_top_level_files(request):
    """Remove irrelevant to selected docs builder files, that are outside docs folder."""
    for irrelevant_to_builder_file in [
        x
        for builder_id, files in DOCS_FILES_EXTRA.items()
        if builder_id != request.docs_website['builder']
        for x in files
    ]:
        os.remove(os.path.join(request.project_dir, irrelevant_to_builder_file))


def _delete_files(files_to_remove):
    """Delete a list of files if they exist."""
    for file in files_to_remove:
        Path(file).unlink(missing_ok=True)


###### LOG FILE REMOVAL


def _take_care_of_logs(logs_file: Path):
    """Remove accidental App Log file, if found inside the Generated Project.

    Ensures that only the Template Files are part of the Generated Projects by
    removing any log file that might have been created during the Generation
    process.

    The application (generator) logs are configured at runtime in _logging.py
    which could cause the cookiecutter's code to inherit our root Logger.

    Then probably, cookiecutter changes the CWD at runtime when it renders the
    Templates, and thus a log file is created inside the Generated Project
    Folder, too.

    # Note: at Generator runtime, the user should still expect Captured Logs to
    # be written a File in their Shell's PWD, as designed and intented.
    """
    # remove the log file if it is empty
    # unintentional behaviour, is still happening
    if logs_file.stat().st_size == 0:  # at least expect empty log file
        try:  # safely remove the empty log file
            logs_file.unlink()
        except PermissionError as e:  # has happened on Windows CI
            # PermissionError: [WinError 32] The process cannot access the
            # file because it is being used by another process
            logger.debug(
                "Permission Error, when removing empty log file: %s",
                json.dumps(
                    {
                        'file': str(logs_file),
                        'error': str(e),
                        'platform': str(sys.platform),
                    },
                    indent=4,
                    sort_keys=True,
                ),
            )
    else:  # captured logs were written in the file: shy from removing it
        # Tell user about this, and let them decide what to do
        print(f"[INFO]: Captured Logs were written in {logs_file}")


## COMMIT ##
def iter_files(request):
    path_obj = Path(request.project_dir)
    for file_path in path_obj.rglob('*'):
        if bool(
            path.isfile(file_path)
            and '__pycache__' not in str(file_path)
            and str(os.path.relpath(file_path, start=request.project_dir)) != '.git'
            and not str(os.path.relpath(file_path, start=request.project_dir)).startswith(
                '.git/'
            )
        ):
            yield str(file_path)


def git_commit(request):
    """Commit the staged changes in the generated project."""
    cookiecutter_config_str = (
        '\n'.join((f"  {key}: {val}" for key, val in request.vars.items())) + '\n'
    )
    commit_message = (
        "Template applied from"
        " https://github.com/boromir674/cookiecutter-python-"
        "package\n\n"
        "Template configuration:\n"
        f"{cookiecutter_config_str}"
    )

    request.repo.index.add(
        list(iter((path.relpath(x, start=request.project_dir) for x in iter_files(request))))
    )
    author = Actor(request.vars['author'], request.vars['author_email'])

    request.repo.index.commit(commit_message, author=author, committer=copy(author))


###### POST HOOK


def post_hook():
    """Delete irrelevant to Project Type files and optionally do git commit."""
    request = get_request()

    # Step 1: Remove irrelevant files
    post_file_removal(request)

    # Step 2: Handle accidental log files
    _handle_logs(request)

    # Step 3: Initialize Git repository and commit changes
    _initialize_and_commit_git_repo(request)
    return 0


def _handle_logs(request):
    """Handle accidental log files created during project generation."""
    potentially_spawned_log_file = Path(request.project_dir) / FILE_TARGET_LOGS
    if potentially_spawned_log_file.exists():
        _take_care_of_logs(potentially_spawned_log_file)


def _initialize_and_commit_git_repo(request):
    """Initialize a Git repository and commit changes if required."""
    if not git_binary_found:
        print(
            "\n"
            "\033[93m[WHAT HAPPENED]\033[0m An error occurred during the Git Repo initialization process.\n"
            "\033[94m[HOW IT HAPPENED]\033[0m The library '\033[92mgitpython\033[0m' attempted to invoke the Git binary but failed.\n"
            "\033[95m[WHY IT HAPPENED]\033[0m The Git binary is missing or not accessible in your system's PATH.\n"
            "\033[96m[HOW TO FIX]\033[0m Install the Git binary on your system:\n"
            "  - For Linux: \033[92msudo apt install git\033[0m or \033[92msudo yum install git\033[0m\n"
            "  - For macOS: \033[92mbrew install git\033[0m\n"
            "  - For Windows: Download and install Git from \033[94mhttps://git-scm.com\033[0m\n"
            "\033[96m[WHAT HAPPENS NEXT]\033[0m Skipping 'git init and 'commit' process\n"
        )
        return

    if request.initialize_git_repo:
        _try_to_commit_changes(request)


def _try_to_commit_changes(request):
    """Attempt to initialize a Git repository and commit changes."""
    repo = Repo.init(request.project_dir)  # do 'git init'
    try:
        is_dirty = repo.is_dirty()  # this raises error if no proper ownership
    except Exception as error:
        _handle_git_error(error)
    else:
        _process_commit(request, repo, is_dirty)


def _handle_git_error(error):
    """Handle errors that occur during Git operations."""
    print(
        "\n"
        f"\033[93m[Exception]\033[0m {error}.\n"
        "\033[93m[Git Diff failed]\033[0m An error occurred while running \033[94m'git diff'\033[0m.\n"
        "\033[94m[HOW IT HAPPENED]\033[0m The library '\033[92mgitpython\033[0m' attempted to invoke the Git binary but failed.\n"
        "\033[96m[How to fix]\033[0m Run 'git config --global --add safe.directory '\n"
        "\033[96m[WHAT HAPPENS NEXT]\033[0m Skipping 'git init and 'commit' process\n"
    )


def _process_commit(request, repo, is_dirty):
    """Process the Git commit if the repository is initialized successfully."""
    if not is_dirty:  # No uncommitted changes
        print(f"\n - {request.project_dir} has no uncommitted changes.")
        request.repo = repo
        git_commit(request)
        print("\033[92m[INFO]\033[0m Git commit was successful.")
    else:  # No changes to commit
        print(f"\n - {request.project_dir} is clean, no changes to commit.")


########


def main():
    """Delete irrelevant to Project Type files and optionally do git commit."""
    sys.exit(post_hook())


if __name__ == "__main__":
    main()
