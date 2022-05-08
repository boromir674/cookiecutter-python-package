import json
import logging
import re
import sys
from typing import Callable, Pattern, Union

IS_PYTHON_PACKAGE: Union[Callable[[str], bool], None]


try:
    from ask_pypi import is_pypi_project

    IS_PYTHON_PACKAGE = is_pypi_project
except ImportError:
    IS_PYTHON_PACKAGE = None


logger = logging.getLogger(__name__)


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


def verify_regex_and_log(message_getter):
    def _verify_regex_and_log(regex: Pattern, string: str):
        if not regex.match(string):
            msg = "RegEx Miss Match Error"
            logger.error(message_getter(msg, regex, string))
            raise RegExMissMatchError(msg)

    return _verify_regex_and_log


def verify_input_with_regex_callback(verify_callback, exception_message=None):
    def verify_input_with_regex(regex: Pattern, string: str):
        try:
            verify_callback(regex, string)
        except RegExMissMatchError as not_matching_regex:
            raise InputValueError(
                exception_message if exception_message else ''
            ) from not_matching_regex

    return verify_input_with_regex


def get_verify_callback(error_message, log_message_getter):
    def _verify_regex(regex: Pattern, string: str):
        verify_input_with_regex_callback(
            verify_regex_and_log(log_message_getter), exception_message=error_message
        )(regex, string)

    return _verify_regex


def verify_templated_semantic_version(version: str):
    REGEX = re.compile(
        r'^(?P<major>0|[1-9]\d*)'
        r'\.'
        r'(?P<minor>0|[1-9]\d*)'
        r'\.'
        r'(?P<patch>0|[1-9]\d*)'
        r'(?:-'
        r'(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+'
        r'(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    )

    def log_message(error, regex, string):
        return (
            "%s: %s",
            str(error),
            json.dumps(
                {
                    'semver_regex': str(regex.pattern),
                    'version_string': str(string),
                }
            ),
        )

    get_verify_callback(
        error_message='Expected a Semantic Version value',
        log_message_getter=log_message,
    )(REGEX, version)


def verify_templated_module_name(module: str):
    REGEX = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]+$')

    def log_message(error, regex, module):
        return (
            "%s: %s",
            str(error),
            json.dumps(
                {
                    'module_name_regex': str(regex.pattern),
                    'module_name': str(module),
                }
            ),
        )

    get_verify_callback(
        error_message='Expected a valid Python Module name value',
        log_message_getter=log_message,
    )(REGEX, module)


def hook_main(request):
    # CHECK Package Name
    try:
        verify_templated_module_name(request.module_name)
    except InputValueError:
        print('ERROR: %s is not a valid Python module name!' % request.module_name)
        return 1

    # CHECK Version
    try:
        verify_templated_semantic_version(request.package_version_string)
    except InputValueError:
        print('ERROR: %s is not a valid Semantic Version!' % request.package_version_string)
        return 1

    # CHECK if input package name (cookiecutter.pkg_name) is available on pypi.org
    if IS_PYTHON_PACKAGE is not None:  # if requirements have been installed
        try:
            search_result = {True: 'not-available', False: 'available'}[
                IS_PYTHON_PACKAGE(request.pypi_package)
            ]
            if search_result == 'not-available':
                print(
                    "Package with name '{name}' already EXISTS on pypi.org!".format(
                        name=request.pypi_package
                    )
                )
                print("You shall rename your Python Package before publishing to pypi!")
            elif search_result == 'available':
                print(
                    "Name '{name}' IS available on pypi.org!".format(name=request.pypi_package)
                )
                print("You will be able to publish your Python Package on pypi as it is!")
        except Exception as error:  # ie network failure
            print(str(error), file=sys.stderr)

    return 0


def _main():
    request = get_request()
    return hook_main(request)


def main():
    sys.exit(_main())


class RegExMissMatchError(Exception):
    pass


class InputValueError(Exception):
    pass


if __name__ == "__main__":
    main()
