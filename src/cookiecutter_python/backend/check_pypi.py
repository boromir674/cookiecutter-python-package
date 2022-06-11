import json
import logging
import typing as t

from requests_futures.sessions import FuturesSession

from cookiecutter_python.backend.user_config_proxy import get_user_config

logger = logging.getLogger(__name__)


def check_pypi(config_file, default_config):
    if config_file and not default_config:
        session = FuturesSession()
        # TODO Improvement: enable feature regardless of default_config
        name = _get_package(get_user_config(config_file, default_config))
        check_pypi_future = session.get(f'http://pypi.org/project/{name}')
        return check_pypi_future, name
    return None, None


def _get_package(context: t.Mapping) -> str:
    default_context = context['default_context']
    variable_name = 'pkg_name'
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
