import logging
import typing as t

from cookiecutter_python.handle.interpreters_support import handle as get_interpreters

from .load_config import get_interpreters_from_yaml

GivenInterpreters = t.Mapping[str, t.Sequence[str]]

logger = logging.getLogger(__name__)


def supported_interpreters(config_file: str, no_input: bool) -> t.Optional[GivenInterpreters]:
    # Interactive Mode: ask for user input with Interactive (console) Dialog
    if not no_input:  # render checkbox console ui, and return user selection
        # TODO: verify that the below works!
        return check_box_dialog(config_file=config_file)
    # NON Interactive Mode: try to automatically read interpreters from config
    if config_file:
        # read 'default_context.interpreters' from User Config yaml file
        return get_interpreters_from_yaml(config_file)
    ## No User Config yaml file, was supplied through CLI parameters, at runtime
    return None


def check_box_dialog(config_file: t.Optional[str] = None) -> GivenInterpreters:
    defaults: t.Optional[t.Sequence[str]] = None
    if config_file:
        interpreters_data: t.Optional[GivenInterpreters] = get_interpreters_from_yaml(
            config_file
        )
        if interpreters_data:
            defaults = interpreters_data.get('supported-interpreters', None)
    return get_interpreters(choices=defaults)
