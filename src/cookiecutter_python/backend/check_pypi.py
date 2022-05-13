from typing import Callable, Union

IS_PYTHON_PACKAGE: Union[Callable[[str], bool], None]


try:
    from ask_pypi import is_pypi_project

    IS_PYTHON_PACKAGE = is_pypi_project
except ImportError:
    IS_PYTHON_PACKAGE = None


def is_registered_on_pypi(package_name: str) -> bool:
    if IS_PYTHON_PACKAGE is None:
        raise ImportError("The 'ask_pypi' python package/module is not installed.")
    return IS_PYTHON_PACKAGE(package_name)
