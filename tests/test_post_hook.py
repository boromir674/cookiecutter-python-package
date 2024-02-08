import sys
import typing as t
from pathlib import Path

if sys.version_info >= (3, 8):
    from typing import Literal, Protocol
else:
    from typing_extensions import Protocol
    from typing_extensions import Literal

import pytest


### IMPORTANT ###
# UPDATE every time a NEW Template File is added to the Generator
@pytest.fixture
def emulated_generated_project(
    request_factory,
):
    from os import mkdir, path

    from cookiecutter_python.hooks.post_gen_project import CLI_ONLY, PYTEST_PLUGIN_ONLY

    def _emulated_generated_project(project_dir: str, name: str = 'biskotaki', **kwargs):
        print(f"[DEBUG]: Gen Proj Dir: {project_dir}")
        package_dir = path.join(project_dir, 'src', name)
        tests_dir = path.join(project_dir, 'tests')

        # emulate/create some Project files affecting production code
        mkdir(path.join(project_dir, 'src'))
        mkdir(path.join(project_dir, 'DEL-ME-UNIT-TESTS'))
        mkdir(package_dir)
        mkdir(tests_dir)

        # Emulate Docs Builder related files (ie mkdocs and sphinx)
        mkdir(path.join(project_dir, 'docs-mkdocs'))
        from pathlib import Path

        # Path(path.join(project_dir, 'mkdocs.yml')).touch()

        mkdir(path.join(project_dir, 'docs-sphinx'))
        Path(path.join(project_dir, 'docs-sphinx', 'conf.py')).touch()

        mkdir(path.join(project_dir, 'scripts'))
        # Path(path.join(project_dir, 'scripts', 'gen_api_refs_pages.py')).touch()

        # Generate, for given name and project_dir
        emulated_post_gen_request = request_factory.post(
            project_dir=project_dir,
            initialize_git_repo=True,  # affects post_gen_project.py
            project_type=kwargs.get('project_type', 'module+cli'),
            module_name=name,
        )

        # Automatically, discover what files to create for an accurate emulated project
        ## Project Type Dependend Files ##
        # Types
        class RuntimeRequest(Protocol):
            module_name: str  # runtime value for {{ cookiecutter.pkg_name }}

        UniqueFile = t.Tuple[str, ...]  # One Files of a Project Type
        ProjectUniqueFiles = t.List[UniqueFile]  # All Files of a Project Type

        CreateProjectUniqueFilesList = t.Callable[[RuntimeRequest], ProjectUniqueFiles]
        """EG for 'module+cli' Project Type: lambda x: [
            ('src', x.module_name, 'cli.py'),
            ('src', x.module_name, '__main__.py'),
            ('tests', 'test_cli.py'),
            ('tests', 'test_invoking_cli.py'),
        ]"""
        # TODO: Create Single Source of Truth (SoT), both to read here and for Post Removal
        # to read in Post Gen Hook
        # SEE 'get_docs_gen_internal_config', SoT solution for Docs post Removal

        ProjectType = Literal['module+cli', 'pytest-plugin']
        ProjectUniqueFilesMap = t.Dict[ProjectType, CreateProjectUniqueFilesList]

        # ProjectUniqueFilesMap = t.Dict[str, CreateProjectUniqueFilesList]
        expected_post_removal: ProjectUniqueFilesMap = {
            'module+cli': CLI_ONLY,
            'pytest-plugin': PYTEST_PLUGIN_ONLY,
        }

        def generate_all_extra_files(
            project_types: ProjectUniqueFilesMap,
        ) -> t.Iterator[UniqueFile]:
            for proj_unique_files_from_request in project_types.values():
                for file_path_parts_tuple in proj_unique_files_from_request(
                    emulated_post_gen_request
                ):
                    yield file_path_parts_tuple

        ## All files expected to be considered, for Post Removal ##
        extra_files_declared: t.List[UniqueFile] = list(
            (x for x in generate_all_extra_files(expected_post_removal))
        )

        assert isinstance(extra_files_declared, list) and len(extra_files_declared) > 2
        # FILES so far, we should CREATE EMULATED, for Post Removal Hook to work
        create_emulated: t.Set[t.Tuple[str, ...]] = set(extra_files_declared)

        # if someone checks the length of the file list, they expect the number of unique files
        # to be equal to the length of the list
        expected_unique_files = len(create_emulated)
        # Sanity check that no-one inputs the same file twice
        assert len(extra_files_declared) == expected_unique_files

        ## Docs Builder Type Dependend Files ##
        from cookiecutter_python.hooks.post_gen_project import (
            builder_id_2_files as builder_id_2_extra_files_map,
        )

        # theoritically, it should suffice for us to create 'emulated' files, as:
        # Excluding the Docs Builder defined in the Request, create file for all
        # builders in the map
        requested_docs_builder_id: str = emulated_post_gen_request.docs_website['builder']

        assert requested_docs_builder_id == 'sphinx'
        assert builder_id_2_extra_files_map == {
            'mkdocs': ['mkdocs.yml', 'scripts/gen_api_refs_pages.py']
        }
        for builder_id, builder_files in builder_id_2_extra_files_map.items():
            if builder_id != requested_docs_builder_id:
                create_emulated.update([(file_path,) for file_path in builder_files])

        assert len(create_emulated) == expected_unique_files + 2

        expected_unique_files = expected_unique_files + sum(
            [len(x) for x in builder_id_2_extra_files_map.values()]
        )
        # Sanity check that no-one inputs the same file twice
        assert len(create_emulated) == expected_unique_files

        # create all derived files, for Post Remove Hook to work
        for path_tuple in sorted(create_emulated):
            with open(path.join(project_dir, *path_tuple), 'w') as _file:
                _file.write('print("Hello World!")\n')

        return emulated_post_gen_request

    return _emulated_generated_project


@pytest.fixture
def get_post_gen_main(get_object, emulated_generated_project):
    """Get a monkeypatched post_gen_project.main method."""
    from pathlib import Path

    name = 'gg'

    def get_pre_gen_hook_project_main(
        add_cli: bool,
        project_dir: Path,
        extra_files: t.Optional[t.List[t.Union[str, t.Tuple[str, ...]]]] = None,
        extra_non_empty_files: t.Optional[t.List[t.Union[str, t.Tuple[str, ...]]]] = None,
    ):
        """"""

        def mock_get_request():
            # to avoid bugs we require empty project dir, before emulated generation
            absolute_proj_dir = Path(project_dir).absolute()
            assert len(list(absolute_proj_dir.iterdir())) == 0

            # EMULATE a GEN Project, by creating minimal dummy files and folders
            emulated_request = emulated_generated_project(
                project_dir, name=name, project_type='module+cli' if add_cli else 'module'
            )
            # sanity check that sth got generated
            assert len(list(absolute_proj_dir.iterdir())) > 0

            # Emulate Extra Empty files, given specific Test Case Scenario
            if extra_files:
                for _file_path in extra_files:
                    if isinstance(_file_path, str):
                        file_path = (_file_path,)
                    absolute_proj_dir.joinpath(*file_path).touch()

            # Emulate Extra Non-Empty files, given specific Test Case Scenario
            if extra_non_empty_files:
                for _file_path in extra_non_empty_files:
                    if isinstance(_file_path, str):
                        file_path = (_file_path,)
                    with open(absolute_proj_dir.joinpath(*file_path), 'w') as _file:
                        _file.write('print("Hello World!")\n')

            return emulated_request

        # Get a main method, with a mocked get_request
        # When called, will Generate the Emulated Project, in a just-in-time-manner
        # By monekypatching the `get_request`, with the emulated one
        # the emulated `get_request`, when called,
        # first Generates the Emulated Project, and then returns
        # the Request object
        import sys

        def emulated_exit(exit_code: int):
            assert exit_code == 0
            return exit_code

        # Monkeypatch with MOCKs the 'sys.exit' and 'sys.version_info' objects
        get_object(
            "main",
            "cookiecutter_python.hooks.post_gen_project",
            overrides={
                'sys': lambda: type(
                    'MockedSys',
                    (),
                    {
                        'exit': emulated_exit,
                        'version_info': type(
                            'Mocked_version_info',
                            (),
                            {
                                'minor': sys.version_info.minor,
                            },
                        ),
                    },
                )
            },
        )
        # Monkeypatch with MOCK the 'get_request' function
        main_method = get_object(
            "main",
            "cookiecutter_python.hooks.post_gen_project",
            overrides={'get_request': lambda: mock_get_request},
        )

        return main_method

    return get_pre_gen_hook_project_main


# REQUIRES well maintained emulated generated project (fixtures)
@pytest.mark.parametrize(
    'add_cli',
    (
        True,
        False,
    ),
    ids=['add-cli', 'do-not-add-cli'],
)
def test_main(add_cli, get_post_gen_main, assert_initialized_git, tmpdir):
    """Verify post_gen_project behaviour, with emulated generated project."""
    from pathlib import Path

    # GIVEN a temporary directory, for the emulated generated project
    tmp_target_gen_dir = tmpdir.mkdir('cookiecutter_python.unit-tests.proj-targetr-gen-dir')

    post_hook_main = get_post_gen_main(
        add_cli,
        tmp_target_gen_dir,
    )
    # THEN the Emulated Generated Project, contains all the necessary files
    # that are required for the post_gen_project to run successfully

    # Verify emulated files, which are going to be removed in Post gen Hook, exist
    expexpected_gen_dir = Path(tmp_target_gen_dir).absolute()
    # check for mkdocs.yml file
    # assert (expexpected_gen_dir / 'src').exists()
    # assert (expexpected_gen_dir / 'src').is_dir()
    # assert (expexpected_gen_dir / 'mkdocs.yml').exists()
    # assert (expexpected_gen_dir / 'mkdocs.yml').is_file()

    # Run the Post Gen Hook, with a custom Request, and make sure
    # there is an Emulated Generated Project, with all the necessary files
    # that are required for the post_gen_project to run successfully
    # WHEN the post_gen_project.main is called
    result = post_hook_main()  # raises error, if post gen exit code != 0

    # THEN the post_gen_project.main runs successfully
    assert result is None

    assert_initialized_git(expexpected_gen_dir)


# REQUIRES well maintained emulated generated project (fixtures)
def test_post_file_removal_deletes_empty_logfile_if_found(get_post_gen_main, tmp_path):

    # GIVEN a temporary directory, to store the emulated generated project
    project_dir: Path = tmp_path

    # GIVEN a suitably monkeypatched post_gen_project.main method

    # Emulate placement of empty log file inside the project
    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    extra_files: t.List[str] = [FILE_TARGET_LOGS]

    post_hook_main = get_post_gen_main(
        True,  # True -> with module+cli, else module
        # gen_output_dir,
        tmp_path,
        extra_files=extra_files,
    )

    # WHEN the post_gen_project.main is called
    result = post_hook_main()  # raises error, if post gen exit code != 0

    # THEN the post_gen_project.main runs successfully
    assert result is None

    # AND the Logs File is deleted in Post Gen Hook, since it is empty
    assert not (project_dir / FILE_TARGET_LOGS).exists()


# REQUIRES well maintained emulated generated project (fixtures)
def test_post_file_removal_keeps_logfile_if_found_non_empty(get_post_gen_main, tmp_path):

    # GIVEN a temporary directory, to store the emulated generated project
    project_dir: Path = tmp_path

    # GIVEN a suitably monkeypatched post_gen_project.main method

    # Emulate placement of empty log file inside the project
    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    post_hook_main = get_post_gen_main(
        True,  # True -> with module+cli, else module
        # gen_output_dir,
        tmp_path,
        extra_non_empty_files=[FILE_TARGET_LOGS],
    )

    # WHEN the post_gen_project.main is called
    result = post_hook_main()  # raises error, if post gen exit code != 0

    # THEN the post_gen_project.main runs successfully
    assert result is None

    # AND the Logs File is kept during Post Gen Hook, since it is not empty
    assert (project_dir / FILE_TARGET_LOGS).exists()
    assert (project_dir / FILE_TARGET_LOGS).is_file()
    assert (project_dir / FILE_TARGET_LOGS).stat().st_size > 0
