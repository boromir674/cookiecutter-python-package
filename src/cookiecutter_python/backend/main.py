import io
import json
import logging
import os
import sys
import typing as t

import poyo
from cookiecutter.exceptions import InvalidConfiguration
from requests.exceptions import ConnectionError, JSONDecodeError

from cookiecutter_python.backend.check_pypi import check_pypi
from cookiecutter_python.backend.check_pypi_handler import handler

from .cookiecutter_proxy import cookiecutter

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


def load_yaml(config_file) -> t.Mapping:
    # TODO use a proxy to load yaml
    with io.open(config_file, encoding='utf-8') as file_handle:
        try:
            yaml_dict = poyo.parse_string(file_handle.read())
        except poyo.exceptions.PoyoException as error:
            raise InvalidConfiguration(
                'Unable to parse YAML file {}. Error: {}' ''.format(config_file, error)
            ) from error
    return yaml_dict


GivenInterpreters = t.Mapping[str, t.Sequence[str]]


def supported_interpreters(config_file, no_input) -> t.Optional[GivenInterpreters]:
    if not no_input:  # interactive
        if sys.version_info < (3, 10):
            check_box_dialog(config_file=config_file)
        # else return None: let generator backend (ie cookiecutter) handle
        # receiving the 'supported-interpreters' information from user input
    # non-interactive
    if config_file:
        try:
            return get_interpreters_from_yaml(config_file)
        except (
            InvalidConfiguration,
            UserConfigFormatError,
            NoInterpretersInUserConfigException,
            JSONDecodeError,
        ):
            pass
    return None


def check_box_dialog(config_file=None) -> GivenInterpreters:
    from cookiecutter_python.handle.interpreters_support import (
        handle as get_interpreters,
    )

    defaults = None
    if config_file:
        try:
            defaults = get_interpreters_from_yaml(config_file)['supported-interpreters']
        except (
            InvalidConfiguration,
            UserConfigFormatError,
            NoInterpretersInUserConfigException,
            JSONDecodeError,
        ):
            pass
    return get_interpreters(choices=defaults)


def get_interpreters_from_yaml(config_file: str) -> GivenInterpreters:
    """Parse the 'interpreters' variable out of the user's config yaml file.

    Args:
        config_file (str): path to the user's config yaml file

    Raises:
        InvalidConfiguration: if yaml parser fails to load the user's config
        UserConfigFormatError: if yaml doesn't contain the 'default_context' key
        NoInterpretersInUserConfigException: if yaml doesn't contain the
            'interpreters' key, under the 'default_context' key
        JSONDecodeError: if json parser fails to load the 'interpreters' value

    Returns:
        GivenInterpreters: dictionary with intepreters as a sequence of strings,
            mapped to the 'supported-interpreters' key
    """
    data = load_yaml(config_file)
    if 'default_context' not in data:
        raise UserConfigFormatError(
            "User config (is valid yaml but) does not contain a 'default_context' outer key!"
        )
    context = data['default_context']
    if 'interpreters' not in context:
        raise NoInterpretersInUserConfigException(
            "No 'interpreters' key found in user's config (under the 'default_context' key)."
        )
    interpreters_data = json.loads(context['interpreters'])
    if 'supported-interpreters' not in interpreters_data:
        raise UserConfigFormatError(
            "User config (is valid yaml but) does not contain a "
            "'supported-interpreters' key in the 'interpreters' key"
        )
    return {'supported-interpreters': interpreters_data['supported-interpreters']}


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


class UserConfigFormatError(Exception):
    pass


class NoInterpretersInUserConfigException(Exception):
    pass
