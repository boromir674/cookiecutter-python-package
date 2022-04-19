import re
import sys


def check_module_name_is_valid_python_module_name(module):
    MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

    if not re.match(MODULE_REGEX, module):
        print('ERROR: %s is not a valid Python module name!' % module)

        # exits with status 1 to indicate failure
        sys.exit(1)


def check_version_is_semver(version):
    REGEX = re.compile('^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')
    if not REGEX.match(version):
        print('ERROR: %s is not a valid Semantic Version!' % version)
        sys.exit(1)



# CHECK Package Name

# the name the client code shall use to import the package
package_name = '{{ cookiecutter.pkg_name }}'

check_module_name_is_valid_python_module_name(package_name)


# CHECK Version

package_version = '{{ cookiecutter.version }}'

check_version_is_semver(package_version)
