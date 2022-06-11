import logging
import os

from requests.exceptions import ConnectionError

from .check_pypi import check_pypi
from .check_pypi_handler import handler
from .generator import create_context, generator
from .helpers import supported_interpreters

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

    # first request is started in background
    check_future, pkg_name = check_pypi(config_file, default_config)

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
    if pkg_name:
        try:  # evaluate future by waiting, only if needed!
            handler(lambda x: check_future.result().status_code == 200)(pkg_name)
        except ConnectionError as error:
            raise CheckPypiError("Connection error while checking PyPi") from error
    print('Finished :)')
    return project_dir


class CheckPypiError(Exception):
    pass
