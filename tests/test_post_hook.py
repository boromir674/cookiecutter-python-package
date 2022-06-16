import pytest


@pytest.fixture
def get_post_gen_main(get_object, request_factory, tmpdir):
    from os import path
    import os
    name = 'gg'
    def get_pre_gen_hook_project_main(add_cli):
        def mock_get_request():
            # create a file to emulate the generation process
            os.mkdir(path.join(tmpdir, 'src'))
            os.mkdir(path.join(tmpdir, 'src', name))
            with open(path.join(tmpdir, 'src', name, 'cli.py'), 'w') as _file:
                _file.write('print("Hello World!"\n')
            with open(path.join(tmpdir, 'src', name, '__main__.py'), 'w') as _file:
                _file.write('print("Hello World 2"\n')
            return request_factory.post(
                project_dir=tmpdir,
                initialize_git_repo=True,  # affects post_gen_project.py
                add_cli=add_cli,
                module_name=name,
            )
        main_method = get_object(
            "_post_hook",
            "cookiecutter_python.hooks.post_gen_project",
            overrides={'get_request': lambda: mock_get_request},
        )
        return main_method

    return get_pre_gen_hook_project_main


@pytest.mark.parametrize('add_cli', (
    True,
    False,
))
def test_main(add_cli, get_post_gen_main, assert_initialized_git, tmpdir):
    post_hook_main = get_post_gen_main(add_cli)
    result = post_hook_main()
    assert result == 0
    assert_initialized_git(tmpdir)
