import logging
import os

from requests.exceptions import ConnectionError

from .generator import create_context, generator
from .helpers import supported_interpreters
from .hosting_services import Engine

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


WEB_SERVERS = ['pypi', 'readthedocs']


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

    check_results = check.check(WEB_SERVERS)

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
    for result in check_results:
        try:
            check.handle(result)
        except ConnectionError as error:
            raise CheckWebServerError(
                f"Connection error while checking {result.service_name} web server"
            ) from error

    print('Finished :)')
    return project_dir


class CheckWebServerError(Exception):
    pass
