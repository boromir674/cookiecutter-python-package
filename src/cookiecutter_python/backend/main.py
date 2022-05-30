import logging
import os
import sys
import json
import typing as t
from requests.exceptions import ConnectionError, JSONDecodeError

from cookiecutter_python.backend.check_pypi import check_pypi
from cookiecutter_python.backend.check_pypi_handler import handler

from .cookiecutter_proxy import cookiecutter

logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


def load_yaml(config_file):
    import io
    import poyo
    from cookiecutter.exceptions import InvalidConfiguration
    with io.open(config_file, encoding='utf-8') as file_handle:
        try:
            yaml_dict = poyo.parse_string(file_handle.read())
        except poyo.exceptions.PoyoException as e:
            raise InvalidConfiguration(
                'Unable to parse YAML file {}. Error: {}' ''.format(config_file, e)
            )
    return yaml_dict

def supported_interpreters(config_file, no_input) -> t.Sequence[str]:
    if not no_input:  # interactive
        if not config_file:
            print(sys.version_info)
            print(sys.version_info < (3, 10))
            if sys.version_info < (3, 10):
                return check_box_dialog()
            # else let cookiecutter cli handle!
        else:
            return check_box_dialog(config_file=config_file)

    else:  # non-interactive
        if not config_file:  # use cookiecutter.json for values
            return None
        else:
            return get_interpreters_from_yaml(config_file)


def check_box_dialog(config_file=None) -> t.Mapping[str, t.Sequence[str]]:
    from cookiecutter_python.handle.interpreters_support import handle as get_interpreters
    defaults = None
    if config_file:
        defaults = get_interpreters_from_yaml(config_file)['supported-interpreters']
    return get_interpreters(choices=defaults)


def get_interpreters_from_yaml(config_file: str) -> t.Optional[t.Mapping[str, t.Sequence[str]]]:
    data = load_yaml(config_file)
    context = data['default_context']
    try:  # use user's config yaml for default values in checkbox dialog
        interpreters_data = json.loads(context['interpreters'])
        return {'supported-interpreters': interpreters_data['supported-interpreters']}
    except (KeyError, JSONDecodeError, Exception) as error:
        print(error)
        print("Could not find 'interpreters' in user's config yaml")


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

    # we handle the interactive input from user here, since cookiecutter does
    # not provide a user-friendly interface for (our use case) the
    # 'interpreters' template variable
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
