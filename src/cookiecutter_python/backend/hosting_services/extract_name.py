import json
from typing import Callable, Mapping

import attr

from ..user_config_proxy import get_user_config
from .exceptions import ContextVariableDoesNotExist
from .value_extractor import BaseValueExtractor


# The Dict Schema expected to be parsed
# class GeneratorYamlData(TypedDict):
#     default_context: Dict[str, Any]


@attr.s(auto_attribs=True, slots=True, frozen=True)
class NameExtractor:
    """Extract Context Value, from a User's Config (YAML) file."""

    name_extractor: Callable[[Mapping], str]

    def __call__(self, config_file: str) -> str:
        # Delegate to Cookiecutter YAML parsing of User Config
        # config_data: GeneratorYamlData = get_user_config(
        config_data = get_user_config(
            config_file=config_file,
            # MUST be False, otherwise Cookiecutter does not do YAML parsing
            default_config=False,
        )
        context_data = config_data['default_context']
        try:
            return self.name_extractor(context_data)
        except KeyError as error:
            raise ContextVariableDoesNotExist(
                "{msg}: {data}".format(
                    msg="Attempted to retrieve non-existant variable",
                    data=json.dumps(
                        {
                            'variable_name': str(self.name_extractor),
                            'available_variables': '[{keys}]'.format(
                                keys=', '.join(
                                    tuple(sorted([str(x) for x in context_data.keys()]))
                                ),
                            ),
                        },
                        indent=4,
                        sort_keys=True,
                    ),
                ),
            ) from error

    @staticmethod
    def create(hosting_service_info):
        return NameExtractor(BaseValueExtractor(hosting_service_info.variable_name))
