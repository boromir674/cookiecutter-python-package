import json
import logging
import typing as t

from requests_futures.sessions import FuturesSession

from cookiecutter_python.backend.user_config_proxy import get_user_config

logger = logging.getLogger(__name__)


def check_readthedocs(config_file, default_config):
    print('---------------')
    print(config_file and not default_config)
    if config_file and not default_config:
        session = FuturesSession()
        # TODO Improvement: enable feature regardless of default_config
        try:
            readthedocs_project_slug = _get_readthedocs_slug(
                get_user_config(config_file, default_config)
            )
            check_readthedocs_future = session.get(
                'https://{readthedocs_project_slug}.readthedocs.io/'.format(
                    readthedocs_project_slug=readthedocs_project_slug,
                )
            )
            return check_readthedocs_future, readthedocs_project_slug
        except ContextVariableDoesNotExist as error:
            print(error)
    return None, None


def _get_readthedocs_slug(context: t.Mapping) -> str:
    default_context = context['default_context']
    variable_name = 'readthedocs_project_slug'
    try:
        return default_context[variable_name]
    except KeyError as error:
        raise ContextVariableDoesNotExist(
            "{msg}: {data}".format(
                msg="Attempted to retrieve non-existant variable",
                data=json.dumps(
                    {
                        'variable_name': str(variable_name),
                        'available_variables': '[{keys}]'.format(
                            keys=', '.join(
                                tuple(sorted([str(x) for x in default_context.keys()]))
                            ),
                        ),
                    },
                    indent=4,
                    sort_keys=True,
                ),
            ),
        ) from error


class ContextVariableDoesNotExist(Exception):
    pass
