import os

import pytest

MY_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(MY_DIR, 'data')


@pytest.fixture
def is_valid_python_module_name():
    from cookiecutter_python.hooks.pre_gen_project import (
        InputValueError,
        verify_templated_module_name,
    )

    def _is_valid_python_module_name(name: str):
        try:
            verify_templated_module_name(name)
            return True
        except InputValueError:
            return False

    return _is_valid_python_module_name


def generate_package_names(file_path):
    with open(file_path, 'r') as f:
        for line in f.readlines():
            yield line


CORRECT_PACKAGE_NAMES = tuple(
    [
        _
        for _ in generate_package_names(
            os.path.join(TEST_DATA_DIR, 'correct_python_package_names.txt')
        )
    ]
)


@pytest.fixture(params=CORRECT_PACKAGE_NAMES, ids=CORRECT_PACKAGE_NAMES)
def correct_module_name(request):
    return request.param


def test_correct_module_name(correct_module_name, is_valid_python_module_name):
    result = is_valid_python_module_name(correct_module_name.strip())
    assert result == True


@pytest.fixture
def get_main_with_mocked_template(get_object, request_factory):
    def get_pre_gen_hook_project_main(overrides={}):
        main_method = get_object(
            "_main",
            "cookiecutter_python.hooks.pre_gen_project",
            overrides=dict(
                {"get_request": lambda: lambda: request_factory.pre()}, **overrides
            ),
        )
        return main_method

    return get_pre_gen_hook_project_main


# def test_main(get_main_with_mocked_template):
#     result = get_main_with_mocked_template(
#         overrides={
#             # we mock the IS_PYTHON_PACKAGE callable, to avoid dependency on network
#             # we also indicate the package name is NOT found already on pypi
#             'available_on_pypi': lambda: lambda x: None
#         }
#     )()
#     assert result == 0  # 0 indicates successfull executions (as in a shell)


def test_main(get_main_with_mocked_template):
    result = get_main_with_mocked_template()()
    assert result == 0  # 0 indicates successfull executions (as in a shell)


# def test_main_without_ask_pypi_installed(get_main_with_mocked_template):
#     def _is_registered_on_pypi(package_name: str):
#         raise ImportError
#     result = get_main_with_mocked_template(overrides={"is_registered_on_pypi": lambda: _is_registered_on_pypi})()
#     assert result == 0  # 0 indicates successfull executions (as in a shell)


def test_main_with_invalid_module_name(get_main_with_mocked_template, request_factory):
    result = get_main_with_mocked_template(
        overrides={"get_request": lambda: lambda: request_factory.pre(module_name="121212")}
    )()
    assert result == 1  # exit code of 1 indicates failed execution


def test_main_with_invalid_version(get_main_with_mocked_template, request_factory):
    main = get_main_with_mocked_template(
        overrides={
            "get_request": lambda: lambda: request_factory.pre(
                package_version_string="gg0.0.1"
            )
        }
    )
    result = main()
    assert result == 1  # exit code of 1 indicates failed execution


@pytest.mark.network_bound
def test_main_with_found_pre_existing_pypi_package(
    get_main_with_mocked_template, request_factory
):
    result = get_main_with_mocked_template(
        overrides={"get_request": lambda: lambda: request_factory.pre(module_name="so_magic")}
    )()
    assert result == 0  # exit code of 1 indicates failed execution
