"""Pre Cookie Hook: Templated File with jinja2 syntax"""
import json
import logging
import sys
from collections import OrderedDict

from cookiecutter_python.backend import sanitize


logger = logging.getLogger(__name__)


# Minimizes the jinja-controlled python syntax-incopatible surface
# Also, this makes static code analyzers to avoid issues with syntax errors
# due to the templated (dynamically injected) code in this file
def get_context() -> OrderedDict:
    """Get the Context, that was used by the Templating Engine at render time"""
    # Templated Variables should be centralized here for easier inspection
    COOKIECUTTER: OrderedDict = OrderedDict()
    COOKIECUTTER = {{cookiecutter}}  # type: ignore    # pylint: disable=undefined-variable  # noqa: F821
    return COOKIECUTTER


def get_request():
    cookie_dict: OrderedDict = get_context()

    logger.info("Cookiecutter Data: %s", json.dumps(cookie_dict, sort_keys=True, indent=4))

    interpreters = cookie_dict['interpreters']

    # the name the client code should use to import the generated package/module
    module_name: str = cookie_dict['pkg_name']

    return type(
        'PreGenProjectRequest',
        (),
        {
            'module_name': module_name,
            'pypi_package': module_name.replace('_', '-'),
            'package_version_string': cookie_dict['version'],
            'interpreters': interpreters['supported-interpreters'],
        },
    )


class InputSanitizationError(Exception):
    pass


def input_sanitization(request):
    try:
        # CHECK Valid Package Name
        sanitize['module-name'](request.module_name)
        # CHECK Version
        sanitize['semantic-version'](request.package_version_string)
        # CHECK Interpreters
        sanitize['interpreters'](request.interpreters)
    except sanitize.exceptions['module-name'] as error:
        raise InputSanitizationError(
            f'ERROR: {request.module_name} is not a valid Python module name!'
        ) from error
    except sanitize.exceptions['semantic-version'] as error:
        raise InputSanitizationError(
            f'ERROR: {request.package_version_string} is not a valid Semantic Version!'
        ) from error
    except sanitize.exceptions['interpreters'] as error:
        logger.warning(
            "Interpreters Data Error: %s",
            json.dumps(
                {
                    'error': str(error),
                    'interpreters_data': request.interpreters,
                },
                sort_keys=True,
                indent=4,
            ),
        )
        raise InputSanitizationError(
            f"ERROR: {request.interpreters} are not valid 'supported interpreters'!"
        ) from error

    print("Sanitized Input Variables :)")


def hook_main(request):
    try:
        input_sanitization(request)
    except InputSanitizationError as error:
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
