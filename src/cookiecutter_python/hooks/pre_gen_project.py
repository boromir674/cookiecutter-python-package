import re
import sys
from typing import Callable, Union


is_python_package: Union[Callable[[str], bool], None]


try:
    from ask_pypi import is_pypi_project
    is_python_package = is_pypi_project
except ImportError:
    is_python_package = None


# Templated Variables should be centralized here for easier inspection

# the name the client code shall use to import the package
PACKAGE_NAME = '{{ cookiecutter.pkg_name }}'
PACKAGE_VERSION = '{{ cookiecutter.version }}'


REQUEST = type('PreGenProjectRequest', (), {
    'package_name': PACKAGE_NAME,
    'package_version_string': PACKAGE_VERSION,
})


def is_valid_python_module_name(module: str):
    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

    if not re.match(MODULE_REGEX, module):
        return False
    return True


def check_version_is_semver(version: str):
    REGEX = re.compile(r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')
    if not REGEX.match(version):
        print('ERROR: %s is not a valid Semantic Version!' % version)
        sys.exit(1)


def available_package_name(package_name: str) -> str:
    if is_python_package is not None:
        try:
            return {True: 'not-available', False: 'available'}[is_python_package(package_name)]
        except Exception as error:  # ie network failure
            print(str(error), file=sys.stderr)
    return 'unknown'


def main(request):
    # CHECK Package Name
    if not is_valid_python_module_name(request.package_name):
        print('ERROR: %s is not a valid Python module name!' % request.package_name)
        # exits with status 1 to indicate failure
        sys.exit(1)

    # CHECK Version
    check_version_is_semver(request.package_version_string)

    search_result = available_package_name(request.package_name)

    print('Package Found?', search_result)
    if search_result == 'not-available':
        print("Package with name '{name}' already EXISTS on pypi.org!".format(name=request.package_name))
        print("You will have to rename your Python Package in order to publish it on pypi!")
    elif search_result == 'available':
        print("Name '{name}' IS available on pypi.org!".format(name=request.package_name))
        print("You will be able to publish your Python Package on pypi as it is!")


if __name__ == "__main__":
    main(REQUEST)
