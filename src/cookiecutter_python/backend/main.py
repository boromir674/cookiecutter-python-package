import logging
import os
import sys
import typing as t

from requests.exceptions import ConnectionError

from cookiecutter_python.backend.check_pypi import check_pypi
from cookiecutter_python.backend.check_pypi_handler import handler
from cookiecutter_python.backend.load_config import get_interpreters_from_yaml
from cookiecutter_python.handle.interpreters_support import handle as get_interpreters

from .cookiecutter_proxy import cookiecutter

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


GivenInterpreters = t.Mapping[str, t.Sequence[str]]


def supported_interpreters(config_file, no_input) -> t.Optional[GivenInterpreters]:
    if not no_input:  # interactive
        if sys.version_info < (3, 10):
            return check_box_dialog(config_file=config_file)
        return None
    if config_file:
        return get_interpreters_from_yaml(config_file)
    return None


def check_box_dialog(config_file=None) -> GivenInterpreters:
    defaults: t.Optional[t.Sequence[str]] = None
    if config_file:
        interpreters_data: t.Optional[GivenInterpreters] = get_interpreters_from_yaml(
            config_file
        )
        if interpreters_data:
            defaults = interpreters_data.get('supported-interpreters', None)
    return get_interpreters(choices=defaults)


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

    template: str = os.path.abspath(os.path.join(my_dir, '..'))

    interpreters = supported_interpreters(config_file, no_input)
    print('Interpreters Data:', interpreters)

    if interpreters:  # update extra_context
        # supported interpreters supplied either from yaml or from user's input
        if extra_context:
            new_context = dict(
                extra_context,
                **{
                    'interpreters': interpreters,
                }
            )
        else:
            new_context = {
                'interpreters': interpreters,
            }
    else:
        new_context = extra_context

    project_dir = cookiecutter(
        template,
        checkout=checkout,
        no_input=no_input,
        extra_context=new_context,
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
    print('Finished :)')
    return project_dir


class CheckPypiError(Exception):
    pass
