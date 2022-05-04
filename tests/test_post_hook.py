import os
import pytest


@pytest.fixture
def get_main_with_mocked_template(get_object, request_factory):
    def get_pre_gen_hook_project_main(overrides={}):
        main_method = get_object(
            'main',
            'cookiecutter_python.hooks.post_gen_project',
            # overrides=dict({
            #     'get_request': lambda: lambda: request_factory.post()}, **overrides)
            )
        return lambda: main_method(request_factory.post(
            project_dir='dummy_folder', # TODO find out if we can use a temp dir
            initialize_git_repo=False,
        ))
        # return main_method
    return get_pre_gen_hook_project_main


@pytest.fixture
def get_main(get_main_with_mocked_template):
    # def main(_main):
    #     try:
    #        _main
    #     except SystemExit as error:

    return get_main_with_mocked_template


def test_main(get_main):
    try:
        result = get_main()()
    except SystemExit as error:
        result = error.code
    assert result == 0
