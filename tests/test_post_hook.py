import typing as t
from pathlib import Path

import pytest


## TYPES


# Automatically, discover what files to create for an accurate emulated project
## Project Type Dependend Files ##
# Types
class RuntimeRequest(t.Protocol):
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

ProjectType = t.Literal['module+cli', 'pytest-plugin']
ProjectUniqueFilesMap = t.Dict[ProjectType, CreateProjectUniqueFilesList]


# Fixture to "reduce complexity" of "create_context_from_emulated_project" fixture
@pytest.fixture
def generate_all_extra_files():
    from cookiecutter_python.hooks.post_gen_project import CICD_DELETE

    def _generate_all_extra_files(
        project_types: ProjectUniqueFilesMap,
        emulated_context: t.Dict[str, str],
    ) -> t.Iterator[UniqueFile]:
        for file_path_parts_tuple in (
            file_path_parts_tuple
            for proj_unique_files_from_request in project_types.values()
            for file_path_parts_tuple in proj_unique_files_from_request(
                type('GG', (), {'module_name': emulated_context['pkg_name']})()
            )
        ):
            assert type(file_path_parts_tuple) is tuple
            yield file_path_parts_tuple
        for path_components_tuple in (
            path_components_tuple
            for cicd_version_unique_files in CICD_DELETE.values()
            for path_components_tuple in cicd_version_unique_files
        ):
            assert type(path_components_tuple) is tuple
            yield path_components_tuple

    return _generate_all_extra_files


### IMPORTANT ###
# UPDATE every time a NEW Template File is added to the Generator
# To increase control on test case behavior, see tests/conftest.py -> 'class HookRequest'
@pytest.fixture
def create_context_from_emulated_project(generate_all_extra_files, dat):
    """Create an emulated Gen Project and return a Request matching it.

    An minimal Project structure is automatically created to emulate the
    generated project state, before the post_get_project hook runs.

    It includes minimal dummy files and folders, but emulates the structure of
    that the app generates, before the post_gen_project "kicks-in".
    """

    #### EMULATED PROJECT STRUCTURE, state before Post Gen Hook
    from os import mkdir, path
    from pathlib import Path

    from cookiecutter_python.hooks.post_gen_project import CLI_ONLY, PYTEST_PLUGIN_ONLY

    def emulate_project_before_post_gen_hook(
        project_dir: str, name: str = 'biskotaki', **kwargs
    ):
        """An emulated Generated Project state, before the post_get_project hook ran.

        It includes minimal dummy files and folders, but emulates the structure of
        that the app generates, before the post_gen_project "kicks-in".

        Returns:
            [type]: [description]

        Yields:
            [type]: [description]
        """
        print(f"[DEBUG]: Gen Proj Dir: {project_dir}")
        package_dir = path.join(project_dir, 'src', name)
        tests_dir = path.join(project_dir, 'tests')

        # emulate/create some Project files affecting production code
        mkdir(path.join(project_dir, 'src'))
        mkdir(path.join(project_dir, 'DEL-ME-UNIT-TESTS'))
        mkdir(package_dir)
        mkdir(tests_dir)

        # Emulate mkdocs Docs Builder related files (as if selected by user)
        mkdir(path.join(project_dir, 'docs'))
        mkdir(path.join(project_dir, 'docs', 'dev_guides'))
        Path(path.join(project_dir, 'docs', 'dev_guides', 'docker.md')).touch()
        # Path(path.join(project_dir, 'mkdocs.yml')).touch()

        # Emulate sphinx Docs Builder related files for sphinx
        TO_DELETE = 'PyGen_TO_DELETE'
        mkdir(path.join(project_dir, TO_DELETE))
        Path(path.join(project_dir, TO_DELETE, 'conf.py')).touch()
        # create at least one level of nest to make cover more post_removal code
        mkdir(path.join(project_dir, TO_DELETE, 'contents'))
        Path(path.join(project_dir, TO_DELETE, 'contents', '10_introduction.rst')).touch()

        mkdir(path.join(project_dir, 'scripts'))
        # Path(path.join(project_dir, 'scripts', 'gen_api_refs_pages.py')).touch()

        # Create .github/workflows directory
        mkdir(path.join(project_dir, '.github'))
        mkdir(path.join(project_dir, '.github', 'workflows'))

        # Generate, for given name and project_dir
        project_type: str = kwargs.pop('project_type', 'module+cli')

        from collections import OrderedDict

        emulated_context = OrderedDict(
            dat,
            **dict(
                project_dir=project_dir,
                initialize_git_repo='yes',  # affects post_gen_project.py
                project_type=project_type,
                pkg_name=name,
                **kwargs,
            ),
        )

        # # Automatically, discover what files to create for an accurate emulated project
        # ## Project Type Dependend Files ##

        # # TODO: Create Single Source of Truth (SoT), both to read here and for Post Removal
        # # to read in Post Gen Hook
        # # SEE 'get_docs_gen_internal_config', SoT solution for Docs post Removal

        # ProjectUniqueFilesMap = t.Dict[str, CreateProjectUniqueFilesList]
        expected_post_removal: ProjectUniqueFilesMap = {
            'module+cli': CLI_ONLY,
            'pytest-plugin': PYTEST_PLUGIN_ONLY,
        }

        ## Generate All files expected to be considered, for Post Removal ##
        extra_files_declared: t.List[UniqueFile] = list(
            (x for x in generate_all_extra_files(expected_post_removal, emulated_context))
        )

        assert isinstance(extra_files_declared, list) and len(extra_files_declared) > 2
        # FILES so far, we should CREATE EMULATED, for Post Removal Hook to work
        create_emulated: t.Set[t.Tuple[str, ...]] = set(extra_files_declared)

        # if someone checks the length of the file list, they expect the number of unique files
        # to be equal to the length of the list
        expected_unique_files = len(create_emulated)
        # Sanity check that no-one inputs the same file twice
        print('\n' + '\n'.join(sorted([str(x) for x in extra_files_declared])) + '\n')
        print('\n' + '\n'.join(sorted([str(x) for x in create_emulated])) + '\n')
        assert (
            len(extra_files_declared) == expected_unique_files
        ), f"{extra_files_declared} != {expected_unique_files}"

        ## Docs Builder Type Dependend Files ##
        from cookiecutter_python.hooks.post_gen_project import (
            DOCS_FILES_EXTRA as builder_id_2_extra_files_map,
        )

        # theoritically, it should suffice for us to create 'emulated' files, as:
        # Excluding the Docs Builder defined in the Request, create file for all
        # builders in the map
        requested_docs_builder_id: str = emulated_context['docs_builder']

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

        return emulated_context

    return emulate_project_before_post_gen_hook


## Helper Fixture for emulating logs file placement, during generation.
@pytest.fixture(scope='session')
def create_dummy_files():
    def _create_dummy_files(
        absolute_proj_dir: Path,
        extra_files: t.Optional[t.List[t.Union[str, t.Tuple[str, ...]]]] = None,
        extra_non_empty_files: t.Optional[t.List[t.Union[str, t.Tuple[str, ...]]]] = None,
    ):
        # Create Extra Empty files, on-demand to support diverse test cases
        for _file_path in extra_files or []:
            assert isinstance(_file_path, str)
            file_path = (_file_path,)
            absolute_proj_dir.joinpath(*file_path).touch()

        # Create Extra files with dummy content, to Emulate, to support diverse test cases
        for _file_path in extra_non_empty_files or []:
            assert isinstance(_file_path, str)
            file_path = (_file_path,)
            with open(absolute_proj_dir.joinpath(*file_path), 'w') as _file:
                _file.write('print("Hello World!")\n')

    return _create_dummy_files


### IMPORTANT ###
# UPDATE every time a NEW Template File is added to the Generator
# To increase control on test case behavior, see tests/conftest.py -> 'class HookRequest'
@pytest.fixture
def get_post_gen_main(create_dummy_files, get_object):
    """Get post_gen_project.main method, with Monkeypatched objects.

    An minimal Project structure is automatically created to emulate the
    generated project state, before the post_get_project hook runs.

    It includes minimal dummy files and folders, but emulates the structure of
    that the app generates, before the post_gen_project "kicks-in".
    """
    from pathlib import Path

    name = 'gg'

    def _emulated_exit(exit_code: int):
        assert exit_code == 0
        return exit_code

    def get_post_gen_hook_project_main(
        context_from_emulated_project,
        add_cli: bool,
        project_dir: Path,
        extra_files: t.Optional[t.List[t.Union[str, t.Tuple[str, ...]]]] = None,
        extra_non_empty_files: t.Optional[t.List[t.Union[str, t.Tuple[str, ...]]]] = None,
        **kwargs,
    ):
        """"""

        # Create Alternative custom Mock Objects to use in Monkeypatch
        from sys import version_info

        _PYTHON_MINOR_VERSION = version_info.minor

        def mock_get_context():
            # to avoid bugs we require empty project dir, before emulated generation
            absolute_proj_dir = Path(project_dir).absolute()
            assert len(list(absolute_proj_dir.iterdir())) == 0

            project_type: str = kwargs.pop(
                'project_type', 'module+cli' if add_cli else 'module'
            )
            # Create a dummy/minimal Project EMULATING file structure, before Post Gen Hook

            emulated_context = context_from_emulated_project(
                project_dir, name=name, project_type=project_type, **kwargs
            )
            assert type(emulated_context['initialize_git_repo']) is not bool
            assert emulated_context['initialize_git_repo'] in {'yes', 'no'}

            # sanity check that sth got generated
            assert len(list(absolute_proj_dir.iterdir())) > 0

            create_dummy_files(
                absolute_proj_dir,
                extra_files=extra_files,
                extra_non_empty_files=extra_non_empty_files,
            )

            # SANITY CHECK that request has cicd str value, otherwise the test cannot continue
            assert isinstance(
                emulated_context['cicd'], str
            ), f"Mocked Request is missing cicd str value: {emulated_context['cicd']}"
            return emulated_context

        # Monkeypatch with MOCKs the 'sys.exit' and 'sys.version_info' objects
        main_method = get_object(
            "main",
            "cookiecutter_python.hooks.post_gen_project",
            overrides={  # objects from above namespace to monkeypatch
                # Monkeypatch the 'get_request' to defer from jinja2 rendering
                # 'get_request': lambda: mock_get_request,
                'get_context': lambda: mock_get_context,
                'GEN_PROJ_LOC': lambda: str(project_dir),
                # Monkeypatch the 'sys' with alternative 'exit' and 'version_info' attributes
                'sys': lambda: type(
                    'MockedSys',
                    (),
                    {
                        'exit': _emulated_exit,
                        'version_info': type(
                            'Mocked_version_info',
                            (),
                            {
                                'minor': _PYTHON_MINOR_VERSION,
                            },
                        ),
                    },
                ),
            },
        )

        return main_method

    return get_post_gen_hook_project_main


# REQUIRES well maintained emulated generated project (fixtures)
@pytest.mark.parametrize(
    'add_cli',
    (
        True,
        False,
    ),
    ids=['add-cli', 'do-not-add-cli'],
)
def test_main(
    add_cli,  # Test Case
    get_post_gen_main,  # CALLABLE to monkeypatch
    # create_request_from_emulated_project,  # REQUEST
    create_context_from_emulated_project,  # CONTEXT
    assert_initialized_git,  # Assertion
    tmpdir,
):
    """Verify post_gen_project behaviour, with emulated generated project."""
    from pathlib import Path

    # GIVEN a temporary directory, for the emulated generated project
    tmp_target_gen_dir = tmpdir.mkdir('cookiecutter_python.unit-tests.proj-targetr-gen-dir')

    post_hook_main = get_post_gen_main(
        create_context_from_emulated_project,
        add_cli,  # control whether to add CLI or not, via request
        tmp_target_gen_dir,
    )
    # THEN the Emulated Generated Project, contains all the necessary files
    # that are required for the post_gen_project to run successfully

    expected_gen_dir = Path(tmp_target_gen_dir).absolute()

    # WHEN the post_gen_project.main is called
    result = post_hook_main()  # raises error, if post gen exit code != 0

    # THEN the post_gen_project.main runs successfully
    assert result is None

    assert_initialized_git(expected_gen_dir)


# REQUIRES well maintained emulated generated project (fixtures)
def test_post_file_removal_deletes_empty_logfile_if_found(
    get_post_gen_main, create_context_from_emulated_project, tmp_path
):
    # GIVEN a temporary directory, to store the emulated generated project
    project_dir: Path = tmp_path

    # GIVEN a suitably monkeypatched post_gen_project.main method

    # Emulate placement of empty log file inside the project
    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    extra_files: t.List[str] = [FILE_TARGET_LOGS]

    post_hook_main = get_post_gen_main(
        create_context_from_emulated_project,
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
def test_post_file_removal_keeps_logfile_if_found_non_empty(
    get_post_gen_main, create_context_from_emulated_project, tmp_path
):
    # GIVEN a temporary directory, to store the emulated generated project
    project_dir: Path = tmp_path

    # GIVEN a suitably monkeypatched post_gen_project.main method

    # Emulate placement of empty log file inside the project
    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    post_hook_main = get_post_gen_main(
        create_context_from_emulated_project,
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


def test_stable_cicd_was_selected_and_worked(
    tmpdir, create_context_from_emulated_project, get_post_gen_main
):
    from pathlib import Path

    # GIVEN a temporary directory, for the emulated generated project
    tmp_target_gen_dir = tmpdir.mkdir('cookiecutter_python.unit-tests.proj-targetr-gen-dir')

    post_hook_main = get_post_gen_main(
        create_context_from_emulated_project,
        False,  # control whether to add CLI or not, via request
        tmp_target_gen_dir,
        # cicd='experimental',
    )
    # WHEN the post_gen_project.main is called
    result = post_hook_main()  # raises error, if post gen exit code != 0

    # THEN the post_gen_project.main runs successfully
    assert result is None

    # AND the .github/workflows.test.yaml file is expected to be found
    assert (Path(tmp_target_gen_dir) / '.github/workflows/test.yaml').exists()
    assert (Path(tmp_target_gen_dir) / '.github/workflows/test.yaml').is_file()

    # AND the files for 'experimental' cicd optoin are missing
    assert not (Path(tmp_target_gen_dir) / '.github/workflows/cicd.yml').exists()
    assert not (Path(tmp_target_gen_dir) / '.github/workflows/codecov-upload.yml').exists()
    assert not (Path(tmp_target_gen_dir) / '.github/workflows/signal-deploy.yml').exists()


def test_experimental_cicd_was_selected_and_worked(
    tmpdir, create_context_from_emulated_project, get_post_gen_main
):
    from pathlib import Path

    # GIVEN a temporary directory, for the emulated generated project
    tmp_target_gen_dir = tmpdir.mkdir('cookiecutter_python.unit-tests.proj-targetr-gen-dir')

    post_hook_main = get_post_gen_main(
        create_context_from_emulated_project,
        False,  # control whether to add CLI or not, via request
        tmp_target_gen_dir,
        cicd='experimental',
    )
    # WHEN the post_gen_project.main is called
    result = post_hook_main()  # raises error, if post gen exit code != 0

    # THEN the post_gen_project.main runs successfully
    assert result is None

    # AND the files for 'experimental' cicd option are present
    assert (Path(tmp_target_gen_dir) / '.github/workflows/cicd.yml').exists()
    assert (Path(tmp_target_gen_dir) / '.github/workflows/cicd.yml').is_file()
    assert (Path(tmp_target_gen_dir) / '.github/workflows/codecov-upload.yml').exists()
    assert (Path(tmp_target_gen_dir) / '.github/workflows/codecov-upload.yml').is_file()
    assert (Path(tmp_target_gen_dir) / '.github/workflows/signal-deploy.yml').exists()
    assert (Path(tmp_target_gen_dir) / '.github/workflows/signal-deploy.yml').is_file()

    # AND the .github/workflows.test.yaml file is missing
    assert not (Path(tmp_target_gen_dir) / '.github/workflows/test.yaml').exists()
    # assert not (Path(tmp_target_gen_dir) / '.github/workflows/test.yaml').is_file()
