import json
import logging
import sys
from collections import OrderedDict

from cookiecutter_python.backend import (
    InputValueError,
    build_input_verification,
    InvalidInterpretersError,
)


logger = logging.getLogger(__name__)


def get_request():
    # Templated Variables should be centralized here for easier inspection
    # Also, this makes static code analyzers to avoid issues with syntax errors
    # due to the templated (dynamically injected) code in this file

    # the name the client code should use to import the generated package/module
    print('\n--- Pre Hook Get Request')

    cookiecutter = OrderedDict()
    cookiecutter: OrderedDict = {{cookiecutter}}

    interpreters = cookiecutter['interpreters']
    if isinstance(interpreters, str):  # we assume it is json
        interpreters = json.loads(interpreters)
    module_name = '{{ cookiecutter.pkg_name }}'

    return type(
        'PreGenProjectRequest',
        (),
        {
            'module_name': module_name,
            'pypi_package': module_name.replace('_', '-'),
            'package_version_string': '{{ cookiecutter.version }}',
            'interpreters': interpreters['supported-interpreters'],
        },
    )


verify_templated_module_name = build_input_verification(
    'module-name',
)

verify_templated_semantic_version = build_input_verification(
    'semantic-version',
)

verify_input_interpreters = build_input_verification(
    'interpreters'
)


def input_sanitization(request):
    # CHECK Package Name
    try:
        verify_templated_module_name(request.module_name)
    except InputValueError as error:
        raise InputValueError(
            f'ERROR: {request.module_name} is not a valid Python module name!'
        ) from error

    # CHECK Version
    try:
        verify_templated_semantic_version(request.package_version_string)
    except InputValueError as error:
        raise InputValueError(
            f'ERROR: {request.package_version_string} is not a valid Semantic Version!'
        ) from error
    try:
        verify_input_interpreters(request.interpreters)
    except InvalidInterpretersError as error:
        logger.warning("Interpreters Data Error: %s", json.dumps({
            'error': error,
            'interpreters_data': request.interpreters,
        }, sort_keys=True, indent=4))
        raise error

    print("Sanitized Input Variables :)")


def hook_main(request):
    try:
        input_sanitization(request)
    except (InputValueError, InvalidInterpretersError) as error:
        print(error)
        return 1
    return 0


def _main():
    request = get_request()
    print('Computed Variables:\n{req}'.format(req=str(request)))
    return hook_main(request)


def main():
    exit_code = _main()
    if exit_code == 0:
        print('Finished Pre Gen Hook :)')
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
