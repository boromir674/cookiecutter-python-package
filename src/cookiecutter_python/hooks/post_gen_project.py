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
except ImportError as error:
    print(error)
    print(
        "Please do 'pip install gitpython' and/or install git binary on host (ie machine, docker)"
    )
import logging

from cookiecutter_python._logging_config import FILE_TARGET_LOGS
from cookiecutter_python.backend.gen_docs_common import get_docs_gen_internal_config


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
        # internally used to get the template folder of each Doc Builder
        'docs_extra_info': DOCS,
    }
    return type('PostGenProjectRequest', (), data)


class PostFileRemovalError(Exception):
    pass


### Define specialized files present per 'project_type' ###
# (ie 'module' or 'module+cli')
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

#     ('.github', 'workflows', 'test.yml'),
# ]
# CICD_STABLE_EXPERIMENTAL = lambda x: [
#     ('.github', 'workflows', 'cicd.yml'),
#     ('.github', 'workflows', 'codecov-upload.yml'),
#     ('.github', 'workflows', 'signal-deploy.yml'),
# ]

# TODO: read from cookiecuuter['_template'] / cookiecutter.json
# delete mkdocs.yml if not using mkdocs
# delete sphinx files if not using sphinx
builder_id_2_files = {
    'mkdocs': ['mkdocs.yml', 'scripts/gen_api_refs_pages.py'],
}


def post_file_removal(request):
    """Preserve only files relevant to Project Type requested to Generate.

    Delete files that are not relevant to the project type requested to
    generate.

    For example, if the user requested a 'module' project type,
    then delete the files that are only relevant to a 'module+cli' project.

    Deletes Files according to CI/CD Pipeline option [stable, experimental]

    Args:
        request ([type]): [description]
    """
    from pathlib import Path

    IRELEVANT_CI_CD_FILES: t.Iterable[t.Tuple[str, ...]] = CICD_DELETE[
        request.vars['cicd']
    ]

    files_to_remove = [
        ## Post-Gen File Removal, given 'Project Type',
        os.path.join(request.project_dir, *x)
        for x in delete_files[request.vars['project_type']](request)
    ] + [
        ## Remove test.tml or cicd.yml based on CI/CD Option ##
        os.path.join(request.project_dir, *path_components)
        for path_components in IRELEVANT_CI_CD_FILES
    ]
    for file in files_to_remove:
        Path(file).unlink(missing_ok=True)  # remove file if exists

    ## Remove gen 'docs' folders, given 'Docs Website Builder' (DWB) ##
    for builder_id, gen_docs_folder_name in request.docs_extra_info.items():
        if builder_id != request.docs_website['builder']:
            shutil.rmtree(str(Path(request.project_dir) / gen_docs_folder_name))

    ## Remove top level files (ie mkdocs.yml), defined in builder_id_2_files map ##
    for builder_id, files in builder_id_2_files.items():
        if builder_id != request.docs_website['builder']:
            for file in files:
                os.remove(os.path.join(request.project_dir, file))


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
    # remove the log file, if it exists and it is empty
    if logs_file.exists():
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


def initialize_git_repo(project_dir: str):
    """
    Initialize the Git repository in the generated project.
    """
    try:
        from git import Repo
    except ImportError as error:  # git binary missing
        raise GitBinaryNotFoundError(error) from error
    return Repo.init(project_dir)


class GitBinaryNotFoundError(Exception):
    pass


def iter_files(request):
    path_obj = Path(request.project_dir)
    for file_path in path_obj.rglob('*'):
        if bool(
            path.isfile(file_path)
            and '__pycache__' not in str(file_path)
            and str(os.path.relpath(file_path, start=request.project_dir)) != '.git'
            and not str(
                os.path.relpath(file_path, start=request.project_dir)
            ).startswith('.git/')
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
        list(
            iter(
                (
                    path.relpath(x, start=request.project_dir)
                    for x in iter_files(request)
                )
            )
        )
    )
    author = Actor(request.vars['author'], request.vars['author_email'])

    request.repo.index.commit(commit_message, author=author, committer=copy(author))


def post_hook():
    """Delete irrelevant to Project Type files and optionally do git commit."""
    request = get_request()
    # Delete gen Files related to
    #  - different Project Type
    #  - related to different documentation builder tool"""
    post_file_removal(request)
    # remove "unintentional logs" file, if it exists and it is empty
    _take_care_of_logs(Path(request.project_dir) / FILE_TARGET_LOGS)

    # "destructure" data
    docs_builder: str = request.docs_extra_info[request.docs_website['builder']]
    
    generated_docs_folder: Path = Path(request.project_dir) / docs_builder
    dest_docs_folder = Path(request.project_dir) / 'docs'

    # V2: supports -f flag, tests pass, but somehow i don't trust it
    # # create if not exists (it might exist if generator invoked with same output path twice)
    # dest_docs_folder.mkdir(parents=True, exist_ok=True)

    # # do a `mv source/* docs/` equivalent operation in python
    # def loop(root_dir: Path):
    #     for file in root_dir.iterdir():
    #         logger.error(f"File: {file}, is file: {file.is_file()}")
    #         if file.is_file():
    #             # Overwrite the file if it exists
    #             shutil.move(str(file), str(dest_docs_folder / file.name))
    #         elif file.is_dir() and str(file) != str(dest_docs_folder):
    #             # Skip the folder if it already exists
    #             target_folder = dest_docs_folder / file.name
    #             if not target_folder.exists():
    #                 shutil.move(str(file), str(target_folder))
    #             loop(file)
    # loop(generated_docs_folder)
    # # remove the empty docs folder, if it exists
    # try:
    #     shutil.rmtree(str(generated_docs_folder))
    #     # generated_docs_folder.rmdir()
    # except OSError as error:
    #     print(f"** Could not remove '{generated_docs_folder}'")
    #     print('Exception: ' + str(error))
    #     raise error    

    # V1: Does not support -f flag, but has been battle-tested
    # move/rename docs-builder-specific docs folder to 'docs/'
    try:
        # ie for mkdocs: `mv docs-mkdocs docs`, ie for sphinx: `mv docs-sphinx docs`
        os.rename(
            str(generated_docs_folder),
            str(dest_docs_folder),
        )
    except OSError as error:  # -f flag passed and -o folder already exists
        # NO SUPPORTED YET
        print(
            "\n"
            f"** Could not move/rename '{docs_builder}' to 'docs/'"
            f"\033[93m[Exception]\033[0m {error}.\n"
            "\033[93m[WHAT HAPPENED]\033[0m An error occurred during the Docs Website generation process.\n"
            "\033[94m[HOW IT HAPPENED]\033[0m The library '\033[92mshutil\033[0m' attempted to move/rename the docs folder but failed.\n"
            "\033[95m[WHY IT HAPPENED]\033[0m The destination folder '\033[92mdocs/\033[0m' already exists.\n"
            "\033[96m[HOW TO FIX]\033[0m Remove the '\033[92mdocs/\033[0m' folder and re-run the command.\n"
            "\033[96m[WHAT HAPPENS NEXT]\033[0m Skipping 'git init and 'commit' process\n"
            "\033[96m[INFO]\033[0m The docs folder was not moved/renamed.\n"
            "\033[96m[INFO]\033[0m The docs folder is still located at: \033[92m{generated_docs_folder}\033[0m\n"
        )
        raise error


    # Git commit
    if request.initialize_git_repo:
        # start process for achieving git commit -m ".."
        try:
            repo = initialize_git_repo(request.project_dir)
        except GitBinaryNotFoundError as error:  # git binary missing
            # print message and skip "git" process
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
        else:  # run only if 'git init' succeeded
            try:
                is_dirty = repo.is_dirty()  # this raises error if no proper ownership
            except Exception as error:  # git config --global --add safe.directory was not executed
                # print message and skip "git" process
                print(
                    "\n"
                    # Print "raw" exception
                    f"\033[93m[Exception]\033[0m {error}.\n"
                    "\033[93m[Git Diff failed]\033[0m An error occurred while running \033[94m'git diff'\033[0m.\n"
                    "\033[94m[HOW IT HAPPENED]\033[0m The library '\033[92mgitpython\033[0m' attempted to invoke the Git binary but failed.\n"
                    "\033[96m[How to fix]\033[0m Run 'git config --global --add safe.directory '\n"
                    "\033[96m[WHAT HAPPENS NEXT]\033[0m Skipping 'git init and 'commit' process\n"
                )
            else:  # runs only if git diff was successful
                # check if the repo is dirty (ie has uncommitted changes)
                if not is_dirty:  # no uncommited changes
                    print(f"\n - {request.project_dir} has no uncommitted changes.")
                    request.repo = repo
                    git_commit(request)
                    print("\033[92m[INFO]\033[0m Git commit was successful.")
                else:  # No changes to commit.
                    # might happen if cli was called twice with same output directory (-o flag)
                    # and with same gen parameters
                    print(
                        f"\n - {request.project_dir} is clean, no changes to commit."
                    )
    return 0


def main():
    """Delete irrelevant to Project Type files and optionally do git commit."""
    sys.exit(post_hook())


if __name__ == "__main__":
    main()
