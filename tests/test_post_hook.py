import pytest


@pytest.fixture
def get_post_gen_main(get_object, request_factory):
    def mock_get_request():
        return request_factory.post(
            project_dir='dummy-folder',  # TODO find out if we can use a temp dir
            initialize_git_repo=False,
            add_cli=True,  # simply to avoid further file processing
        )

    def get_pre_gen_hook_project_main(overrides={}):
        main_method = get_object(
            "_post_hook",
            "cookiecutter_python.hooks.post_gen_project",
            overrides=overrides if overrides else {'get_request': lambda: mock_get_request},
        )
        return main_method

    return get_pre_gen_hook_project_main


def test_main(get_post_gen_main):
    post_hook_main = get_post_gen_main()
    result = post_hook_main()
    assert result == 0
