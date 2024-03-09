import io
import json
import logging
import typing as t
from json import JSONDecodeError

import yaml

GivenInterpreters = t.Mapping[str, t.Sequence[str]]

logger = logging.getLogger(__name__)


def load_yaml(config_file) -> t.MutableMapping:
    # TODO use a proxy to load yaml
    with io.open(config_file, encoding='utf-8') as file_handle:
        try:
            yaml_dict = yaml.safe_load(file_handle)
        # except poyo.exceptions.PoyoException as error:
        except yaml.YAMLError as error:
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

    interpreters = context.get('interpreters')
    if interpreters is None:
        # User Config YAML does not contain 'interpreters' key, can happen if user
        # has not yet set the interpreters in their config file
        return None
    if isinstance(interpreters, str):
        logger.warning(
            "User's YAML is notw expected to contain a dictionary for the 'interpreters' key"
        )
        try:
            return json.loads(context['interpreters'])
        except JSONDecodeError as error:
            # string is not JSON parsable
            logger.warning(
                "User's yaml config 'interpreters' value Error: %s",
                json.dumps(
                    {
                        'error': str(error),
                        'message': "Expected json-parsable value for the 'interpreters' key",
                        'explanation': 'Make sure the value is a valid JSON string',
                    },
                    sort_keys=True,
                    indent=4,
                ),
            )
            return None
    if isinstance(interpreters, dict):
        return interpreters
    raise UserYamlDesignError('Interpreters value is not a string or a dictionary')


class UserYamlDesignError(Exception):
    pass


class InvalidYamlFormatError(Exception):
    pass
