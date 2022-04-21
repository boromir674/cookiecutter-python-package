import os
import pytest


MY_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(MY_DIR, 'data')


@pytest.fixture
def is_valid_python_module_name():
    from cookiecutter_python.hooks.pre_gen_project import is_valid_python_module_name
    return is_valid_python_module_name


def generate_package_names(file_path):
    with open(file_path, 'r') as f:
        for line in f.readlines():
            yield line


CORRECT_PACKAGE_NAMES = tuple([_ for _ in generate_package_names(
    os.path.join(TEST_DATA_DIR, 'correct_python_package_names.txt')
)])

@pytest.fixture(params=CORRECT_PACKAGE_NAMES, ids=CORRECT_PACKAGE_NAMES)
def correct_module_name(request):
    return request.param


def test_correct_module_name(correct_module_name, is_valid_python_module_name):
    result = is_valid_python_module_name(correct_module_name.strip())
    assert result == True



# def test_wrong_module_name