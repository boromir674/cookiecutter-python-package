import io
import json
import logging
import typing as t
from json import JSONDecodeError

import poyo

GivenInterpreters = t.Mapping[str, t.Sequence[str]]

logger = logging.getLogger(__name__)


def load_yaml(config_file) -> t.Mapping:
    # TODO use a proxy to load yaml
    with io.open(config_file, encoding='utf-8') as file_handle:
        try:
            yaml_dict = poyo.parse_string(file_handle.read())
        except poyo.exceptions.PoyoException as error:
            raise InvalidYamlFormatError(
                'Unable to parse YAML file {}. Error: {}' ''.format(config_file, error)
            ) from error
    return yaml_dict


def get_interpreters_from_yaml(config_file: str) -> t.Optional[GivenInterpreters]:
    """Parse the 'interpreters' variable out of the user's config yaml file.

    Args:
        config_file (str): path to the user's config yaml file

    Raises:
        InvalidYamlFormatError: if yaml parser fails to load the user's config
        UserYamlDesignError: if yaml does not contain the 'default_context' key

    Returns:
        GivenInterpreters: dictionary with intepreters as a sequence of strings,
            mapped to the 'supported-interpreters' key
    """
    data = load_yaml(config_file)
    if 'default_context' not in data:
        raise UserYamlDesignError(
            "User config (is valid yaml but) does not contain a 'default_context' outer key!"
        )
    context = data['default_context']
    if 'interpreters' not in context:
        return None

    try:
        interpreters_data = json.loads(context['interpreters'])
    except JSONDecodeError as error:
        logger.warning(
            "User's yaml config 'interpreters' value Error: %s",
            json.dumps(
                {
                    'error': error,
                    'message': "Expected json 'parasable' value for the 'interpreters' key",
                },
                sort_keys=True,
                indent=4,
            ),
        )
        return None
    return interpreters_data


class UserYamlDesignError(Exception):
    pass


class InvalidYamlFormatError(Exception):
    pass
