import io
import json
import logging
import typing as t
from json import JSONDecodeError

import yaml


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


def get_interpreters_from_yaml(
    config_file: str,
) -> t.Optional[t.Mapping[str, t.Sequence[str]]]:
    """Parse the 'interpreters' variable out of the user's config yaml file.

    Args:
        config_file (str): path to the user's config yaml file

    Raises:
        InvalidYamlFormatError: if yaml parser fails to load the user's config
        UserYamlDesignError: if yaml does not contain the 'default_context' key

    Returns:
        t.Mapping[str, t.Sequence[str]]: dictionary with intepreters as a sequence of strings,
            mapped to the 'supported-interpreters' key
    """
    # Step 1: Load YAML data
    data = load_yaml(config_file)

    # Step 2: Validate YAML structure
    context = _validate_and_get_context(data)

    # Step 3: Extract interpreters
    return _extract_interpreters(context)


def _validate_and_get_context(data: t.MutableMapping) -> t.MutableMapping:
    """Validate the YAML structure and return the 'default_context'."""
    if 'default_context' not in data:
        raise UserYamlDesignError(
            "User config (is valid yaml but) does not contain a 'default_context' outer key!"
        )
    return data['default_context']


def _extract_interpreters(
    context: t.MutableMapping,
) -> t.Optional[t.Mapping[str, t.Sequence[str]]]:
    """Extract the interpreters from the 'default_context'."""
    interpreters = context.get('interpreters')

    if interpreters is None:
        # No 'interpreters' key found
        return None

    if isinstance(interpreters, str):
        return _parse_interpreters_from_string(interpreters)

    if isinstance(interpreters, dict):
        return interpreters

    raise UserYamlDesignError('Interpreters value is not a string or a dictionary')


def _parse_interpreters_from_string(
    interpreters: str,
) -> t.Optional[t.Mapping[str, t.Sequence[str]]]:
    """Parse interpreters from a JSON string."""
    logger.warning(
        "User's YAML is now expected to contain a dictionary for the 'interpreters' key"
    )
    try:
        return json.loads(interpreters)
    except JSONDecodeError as error:
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


class UserYamlDesignError(Exception):
    pass


class InvalidYamlFormatError(Exception):
    pass
