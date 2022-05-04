import os
import pytest


MY_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(MY_DIR, 'data')


@pytest.fixture
def is_valid_python_module_name():
    from cookiecutter_python.hooks.pre_gen_project import verify_templated_module_name, InputValueError
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


CORRECT_PACKAGE_NAMES = tuple([_ for _ in generate_package_names(
    os.path.join(TEST_DATA_DIR, 'correct_python_package_names.txt')
)])

@pytest.fixture(params=CORRECT_PACKAGE_NAMES, ids=CORRECT_PACKAGE_NAMES)
def correct_module_name(request):
    return request.param


def test_correct_module_name(correct_module_name, is_valid_python_module_name):
    result = is_valid_python_module_name(correct_module_name.strip())
    assert result == True


@pytest.fixture
def hook_request():
    def __init__(self, **kwargs):
        self.module_name = kwargs.get('module_name', 'awesome_novelty_python_library')
        self.pypi_package = kwargs.get('pypi_package', self.module_name.replace('_', '-'))
        self.package_version_string = kwargs.get('package_version_string', '0.0.1')
    return type('PreGenProjectRequest', (), {'__init__': __init__})


@pytest.fixture
def get_main_with_mocked_template(get_object, hook_request):
    def get_pre_gen_hook_project_main(overrides={}):
        main_method = get_object(
            '_main',
            'cookiecutter_python.hooks.pre_gen_project',
            overrides=dict({
                'get_request': lambda: lambda: hook_request()}, **overrides))
        return main_method
    
    # def get_pre_gen_hook_project_main(**kwargs):
    #     main_method = get_main(**dict({'get_request': lambda: lambda: hook_request()}, **kwargs))
    #     return main_method

    return get_pre_gen_hook_project_main


def test_main(get_main_with_mocked_template):
    result = get_main_with_mocked_template(overrides={
        'is_python_package': lambda: lambda x: False  # we mock to avoid dependency on network
        # we also indicate the package name is NOT found already on pypi
    })()
    assert result == 0  # 0 indicates successfull executions (as in a shell)


@pytest.mark.network_bound
def test_main_with_network(get_main_with_mocked_template):
    result = get_main_with_mocked_template()()
    assert result == 0  # 0 indicates successfull executions (as in a shell)


def test_main_without_ask_pypi_installed(
    get_main_with_mocked_template,
    # get_main,
    # hook_request,
    ):
    # result = get_main_with_mocked_template(is_python_package= lambda: None)()
    result = get_main_with_mocked_template(overrides={
        'is_python_package': lambda: None
    })()
    assert result == 0  # 0 indicates successfull executions (as in a shell)


def test_main_with_invalid_module_name(get_main_with_mocked_template, hook_request):
    result = get_main_with_mocked_template(overrides={
        'get_request': lambda: lambda: hook_request(module_name='121212')
    })()
    assert result == 1  # exit code of 1 indicates failed execution


def test_main_with_invalid_version(get_main_with_mocked_template, hook_request):
    result = get_main_with_mocked_template(overrides={
        'get_request': lambda: lambda: hook_request(package_version_string='gg0.0.1')
    })()
    assert result == 1  # exit code of 1 indicates failed execution


def test_main_with_mocked_found_pre_existing_pypi_package(get_main_with_mocked_template, hook_request):
    result = get_main_with_mocked_template(overrides={
        'is_python_package': lambda: lambda: True,
    })()
    assert result == 0  # exit code of 1 indicates failed execution


@pytest.mark.network_bound
def test_main_with_found_pre_existing_pypi_package(get_main_with_mocked_template, hook_request):
    result = get_main_with_mocked_template(overrides={
        'get_request': lambda: lambda: hook_request(module_name='so_magic')
    })()
    assert result == 0  # exit code of 1 indicates failed execution
