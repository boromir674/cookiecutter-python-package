import os
import typing as t

import pytest

MY_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(MY_DIR, 'data')


@pytest.fixture
def is_valid_python_module_name():
    from cookiecutter_python.hooks.pre_gen_project import sanitize

    def _is_valid_python_module_name(name: str):
        try:
            sanitize['module-name'](name)
            return True
        except sanitize.exceptions['module-name']:
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
    assert result is True


def test_incorrect_module_name(is_valid_python_module_name):
    result = is_valid_python_module_name('23numpy')
    assert not result


def test_prehook_sanitization_throws_error_on_duplicate_interpreters():
    from cookiecutter_python.hooks.pre_gen_project import sanitize

    with pytest.raises(sanitize.exceptions['interpreters']):
        sanitize['interpreters'](["3.10", "3.10"])


def test_prehook_sanitization_throws_error_on_unsupported_interpreters():
    from cookiecutter_python.backend.sanitization.interpreters_support import (
        VALID_PYTHON_VERSIONS,
    )

    SUPPORTED_SET: t.Set[str] = VALID_PYTHON_VERSIONS
    unsupported_interpreter = '3.5'

    # SANITY to make test case valid
    assert unsupported_interpreter not in SUPPORTED_SET

    from cookiecutter_python.hooks.pre_gen_project import sanitize

    with pytest.raises(sanitize.exceptions['interpreters']):
        sanitize['interpreters']([unsupported_interpreter])


def test_prehook_sanitization_passes_given_interpreters_supported_by_gen():
    supported_subset = {"3.8", "3.9", "3.10", "3.11"}
    from cookiecutter_python.hooks.pre_gen_project import sanitize

    sanitize['interpreters'](supported_subset)


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


def test_main_with_invalid_interpreters(get_main_with_mocked_template, request_factory):
    result = get_main_with_mocked_template(
        overrides={
            "get_request": lambda: lambda: request_factory.pre(interpreters=['3.5', '3.10'])
        }
    )()
    assert result == 1  # exit code of 1 indicates failed execution


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


def test_main_with_found_pre_existing_pypi_package(
    get_main_with_mocked_template, request_factory
):
    result = get_main_with_mocked_template(
        overrides={"get_request": lambda: lambda: request_factory.pre(module_name="so_magic")}
    )()
    assert result == 0  # exit code of 1 indicates failed execution
