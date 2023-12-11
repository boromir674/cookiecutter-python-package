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

        Path(path.join(project_dir, 'mkdocs.yml')).touch()

        mkdir(path.join(project_dir, 'docs-sphinx'))
        Path(path.join(project_dir, 'docs-sphinx', 'conf.py')).touch()

        # Generate, for given name and project_dir
        emulated_post_gen_request = request_factory.post(
            project_dir=project_dir,
            initialize_git_repo=True,  # affects post_gen_project.py
            project_type=kwargs.get('project_type', 'module+cli'),
            module_name=name,
        )
        from functools import reduce

        files_set = reduce(
            lambda i, j: i + j,
            (
                # unique files per Project Type
                get_path_tuple(emulated_post_gen_request)  # list of tuples
                for get_path_tuple in [
                    CLI_ONLY,
                    PYTEST_PLUGIN_ONLY,
                ]
            ),
        )

        for path_tuple in files_set:
            with open(path.join(project_dir, *path_tuple), 'w') as _file:
                _file.write('print("Hello World!"\n')
        return emulated_post_gen_request

    return _emulated_generated_project


@pytest.fixture
def get_post_gen_main(get_object, emulated_generated_project):
    """Get a monkeypatched post_gen_project.main method."""
    from pathlib import Path

    name = 'gg'

    def get_pre_gen_hook_project_main(add_cli: bool, project_dir: Path):
        """"""

        def mock_get_request():
            # to avoid bugs we require empty project dir, before emulated generation
            absolute_proj_dir = Path(project_dir).absolute()
            assert len(list(absolute_proj_dir.iterdir())) == 0
            # EMULATE a GEN Project, by craeting minimal dummy files and folders
            emulated_request = emulated_generated_project(
                project_dir, name=name, project_type='module+cli' if add_cli else 'module'
            )
            # sanity check that sth got generated
            assert len(list(absolute_proj_dir.iterdir())) > 0
            return emulated_request

        # Get a main method, with a mocked get_request
        # When called, will Generate the Emulated Project, in a just-in-time-manner
        # By monekypatching the `get_request`, with the emulated one
        # the emulated `get_request`, when called,
        # first Generates the Emulated Project, and then returns
        # the a Request object
        main_method = get_object(
            "_post_hook",
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

    # name = 'gg'

    # def get_pre_gen_hook_project_main(add_cli):
    #     """"""
    #     def mock_get_request():
    #         emulated_request = emulated_generated_project(
    #             tmpdir, name=name, project_type='module+cli' if add_cli else 'module'
    #         )
    #         return emulated_request

    #     main_method = get_object(
    #         "_post_hook",
    #         "cookiecutter_python.hooks.post_gen_project",
    #         overrides={'get_request': lambda: mock_get_request},
    #     )
    #     return main_method
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
    result = post_hook_main()
    # THEN the post_gen_project.main runs successfully
    assert result == 0

    assert_initialized_git(expexpected_gen_dir)
