import sys

from cookiecutter_python.backend.input_sanitization import (
    InputValueError,
    build_input_verification,
)


def get_request():
    # Templated Variables should be centralized here for easier inspection
    # Also, this makes static code analyzers to avoid issues with syntax errors
    # due to the templated (dynamically injected) code in this file

    # the name the client code should use to import the generated package/module
    module_name = '{{ cookiecutter.pkg_name }}'

    return type(
        'PreGenProjectRequest',
        (),
        {
            'module_name': module_name,
            'pypi_package': module_name.replace('_', '-'),
            'package_version_string': '{{ cookiecutter.version }}',
        },
    )


verify_templated_module_name = build_input_verification(
    'module-name',
)

verify_templated_semantic_version = build_input_verification(
    'semantic-version',
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
    print("Sanitized Input Variables :)")


def hook_main(request):
    try:
        input_sanitization(request)
    except InputValueError as error:
        print(error)
        return 1
    return 0


def _main():
    request = get_request()
    return hook_main(request)


def main():
    exit_code = _main()
    if exit_code == 0:
        print('Finished Pre Gen Hook :)')
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
