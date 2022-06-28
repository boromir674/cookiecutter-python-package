import pytest


@pytest.fixture
def post_gen_project_request(request_factory):
    def get_mock_request(project_dir: str, **kwargs):
        return request_factory.post(
            project_dir=project_dir,
            initialize_git_repo=True,  # affects post_gen_project.py
            project_type=kwargs.get('project_type', 'module+cli'),
            module_name=kwargs.get('module_name', 'biskotaki'),
        )

    return get_mock_request


@pytest.fixture
def emulated_generated_project(post_gen_project_request):
    from os import mkdir, path

    from cookiecutter_python.hooks.post_gen_project import CLI_ONLY, PYTEST_PLUGIN_ONLY

    def _emulated_generated_project(project_dir: str, name: str = 'biskotaki', **kwargs):
        package_dir = path.join(project_dir, 'src', name)
        tests_dir = path.join(project_dir, 'tests')
        # emulate/create some Project files affecting production code
        mkdir(path.join(project_dir, 'src'))
        mkdir(package_dir)
        mkdir(tests_dir)

        emulated_post_gen_request = post_gen_project_request(
            project_dir, module_name=name, **kwargs
        )
        from functools import reduce

        files_set = reduce(
            lambda i, j: i + j,
            (
                get_path_tuple(emulated_post_gen_request)
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
def get_post_gen_main(get_object, emulated_generated_project, tmpdir):
    name = 'gg'

    def get_pre_gen_hook_project_main(add_cli):
        def mock_get_request():
            emulated_request = emulated_generated_project(
                tmpdir, name=name, project_type='module+cli' if add_cli else 'module'
            )
            return emulated_request

        main_method = get_object(
            "_post_hook",
            "cookiecutter_python.hooks.post_gen_project",
            overrides={'get_request': lambda: mock_get_request},
        )
        return main_method

    return get_pre_gen_hook_project_main


@pytest.mark.parametrize(
    'add_cli',
    (
        True,
        False,
    ),
    ids=['add-cli', 'do-not-add-cli'],
)
def test_main(add_cli, get_post_gen_main, assert_initialized_git, tmpdir):
    post_hook_main = get_post_gen_main(add_cli)
    result = post_hook_main()
    assert result == 0
    assert_initialized_git(tmpdir)
