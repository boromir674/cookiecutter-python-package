from .helpers import parse_context
from .hosting_services import Engine
from .load_config import get_interpreters_from_yaml


def pre_main(request):
    """Do preparatory steps before the Generation process.

    Makes Request Futures and modifies the Template Context.
    """
    ## External Services Clients Initialization ##
    # clients "how to question" 3rd party web services like pypi, and rtd
    # making http request to web servers hosting endpoints for APIs

    # Checkers are initialized as 'Activated'

    # Activate Async HTTP only if all below are True:
    # - User did not pass the --offline CLI flag
    # - User did not pass the --default-config CLI flag
    # - User passed a Config file YAML

    # Activate: if User Config is given and Default Config is False
    deactivate_signal: bool = bool(request.default_config)
    if request.offline:
        deactivate_signal = True

    request.check = Engine.create(request.config_file, deactivate_signal)

    # Start Requesting Futures! - Hosting Service: PyPI, Read The Docs
    request.check_results = request.check.check(request.web_servers)
    """
    If skipped due to missing info in User Config, we can expect Logs roughly as:
    logger.info(
        "Skipping check of remote server, because of missing context variable"
    )
    logger.info(error)
    """
    _context = request.extra_context or {}
    interactive_mode = not bool(request.no_input)

    # If INTERACTIVE, Run Dialog Pipeline, to update Context
    if interactive_mode:
        # Render Context to be used in Dialogs
        user_input = parse_context(request.config_file)
        _context.update(
            {
                'interpreters': {
                    'supported-interpreters': user_input.pop('supported-interpreters')
                },  # 'supported-interpreters
                # 'supported-interpreters': user_input.pop('supported-interpreters'),
                **user_input,
            }
        )
    elif request.config_file and bool(
        interpreters := get_interpreters_from_yaml(request.config_file)
    ):
        # just update interpreters cookiecutter extra_context
        _context['interpreters'] = interpreters

    request.extra_context = dict(_context)
    return request
