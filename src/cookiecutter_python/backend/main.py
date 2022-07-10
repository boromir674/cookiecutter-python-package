import logging
import os

from requests.exceptions import ConnectionError

from .generator import create_context, generator
from .helpers import supported_interpreters

# from .hosting_services import (
#     check_pypi,
#     check_pypi_handler,
#     check_readthedocs,
#     check_readthedocs_handler,
# )
from .hosting_services import Engine

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


def generate(
    checkout=None,
    no_input=False,
    extra_context=None,
    replay=False,
    overwrite=False,
    output_dir='.',
    config_file=None,
    default_config=False,
    password=None,
    directory=None,
    skip_if_file_exists=False,
) -> str:
    print('Start Python Generator !')
    check = Engine.create(config_file, default_config)
    assert len(check.services_info) == 2
    assert {'pypi', 'readthedocs'} == {str(x.service) for x in check.services_info}
    # check = Checker(config_file, default_config)

    # first request is started in background
    # check_future, pkg_name = check_pypi(config_file, default_config)

    # readthedocs_future, readthedocs_project_slug = check_readthedocs(
    #     config_file, default_config
    # )
    check_pypi_result = check.pypi()
    check_readthedocs_result = check.readthedocs()

    interpreters = supported_interpreters(config_file, no_input)
    if interpreters:  # update extra_context
        # supported interpreters supplied either from yaml or from user's input
        extra_context = create_context(interpreters, extra_context=extra_context)

    project_dir = generator(
        os.path.abspath(os.path.join(my_dir, '..')),  # template dir path
        checkout=checkout,
        no_input=no_input,
        extra_context=extra_context,
        replay=replay,
        overwrite_if_exists=overwrite,
        output_dir=output_dir,
        config_file=config_file,
        default_config=default_config,
        password=password,
        directory=directory,
        skip_if_file_exists=skip_if_file_exists,
    )
    if check_pypi_result:
        try:
            check.handle(check_pypi_result)
        except ConnectionError as error:
            raise CheckWebServerError(
                "Connection error while checking PyPI web server"
            ) from error
    if check_readthedocs_result:
        try:
            check.handle(check_readthedocs_result)
        except ConnectionError as error:
            raise CheckWebServerError(
                "Connection error while checking readthedocs web server"
            ) from error

    # if pkg_name:
    #     try:  # evaluate future by waiting, only if needed!
    #         check.handle_future(check_future)
    #         check_pypi_handler(lambda x: check_future.result().status_code == 200)(pkg_name)
    #     except ConnectionError as error:
    #         raise CheckWebServerError("Connection error while checking PyPi") from error
    # if readthedocs_project_slug:
    #     try:  # evaluate future by waiting, only if needed!
    #         check.handle_future(readthedocs_future)
    #         # check_readthedocs_handler(
    #         #     lambda x: readthedocs_future.result().status_code == 200
    #         # )(readthedocs_project_slug)
    #     except ConnectionError as error:
    #         raise CheckWebServerError(
    #             "Connection error while checking readthedocs.org"
    #         ) from error
    print('Finished :)')
    return project_dir


class CheckWebServerError(Exception):
    pass
