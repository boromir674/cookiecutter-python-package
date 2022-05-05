import pytest


@pytest.fixture
def get_main_with_mocked_template(get_object, request_factory):
    def get_pre_gen_hook_project_main(overrides={}):
        main_method = get_object(
            "main",
            "cookiecutter_python.hooks.post_gen_project",
        )
        return lambda: main_method(
            request_factory.post(
                project_dir="dummy_folder",  # TODO find out if we can use a temp dir
                initialize_git_repo=False,
            )
        )

    return get_pre_gen_hook_project_main


def test_main(get_main_with_mocked_template):
    try:
        result = get_main_with_mocked_template()()
    except SystemExit as error:
        result = error.code
    assert result == 0
