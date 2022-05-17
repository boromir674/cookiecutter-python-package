import json
import logging

from requests_futures.sessions import FuturesSession

from cookiecutter_python.backend.user_config_proxy import get_user_config

logger = logging.getLogger(__name__)


def check_pypi(config_file, default_config):
    if config_file and not default_config:
        session = FuturesSession()
        # TODO Improvement: enable feature regardless of default_config

        default_context = get_user_config(
            config_file=config_file,
            default_config=default_config,
        )['default_context']
        variable_name = 'pkg_name'
        try:
            name = default_context[variable_name]
        except KeyError as error:
            error_msg = "Attempted to retrieve non-existant variable"
            variables = tuple(sorted([str(x) for x in default_context.keys()]))
            logger.debug(
                "%s: %s",
                error_msg,
                json.dumps(
                    {
                        'variable_name': str(variable_name),
                        'available_variables': variables,
                    },
                    indent=4,
                    sort_keys=True,
                ),
            )
            raise ContextVariableDoesNotExist(
                "{msg}: {data}".format(
                    msg=error_msg,
                    data=json.dumps(
                        {
                            'variable_name': str(variable_name),
                            'available_variables': '[{keys}]'.format(
                                keys=', '.join(variables),
                            ),
                        },
                        indent=4,
                        sort_keys=True,
                    ),
                ),
            ) from error
        else:
            check_pypi_future = session.get(f'http://pypi.org/project/{name}')
            return check_pypi_future, name
    return None, None


class ContextVariableDoesNotExist(Exception):
    pass
