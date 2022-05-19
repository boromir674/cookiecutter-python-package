import logging
import os

from requests.exceptions import ConnectionError

from cookiecutter_python.backend.check_pypi import check_pypi
from cookiecutter_python.backend.check_pypi_handler import handler

from .cookiecutter_proxy import cookiecutter

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))


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
    # first request is started in background
    check_future, pkg_name = check_pypi(config_file, default_config)

    template: str = os.path.join(my_dir, '..')

    project_dir = cookiecutter(
        template,
        checkout,
        no_input,
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
        # eval future by waiting only if needed!
        try:
            handler(lambda x: check_future.result().status_code == 200)(pkg_name)
        except ConnectionError as error:
            raise CheckPypiError("Connection error while checking PyPi") from error

    return project_dir


class CheckPypiError(Exception):
    pass
