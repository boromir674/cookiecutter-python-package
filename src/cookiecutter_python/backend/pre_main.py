import typing as t

from .helpers import parse_context
from .hosting_services import Engine


def pre_main(request):
    """Do preparatory steps Generation process, by settings things as the Template Context.

    Args:
        **kwargs: Arbitrary keyword arguments.
    """
    ## External Services Clients Initialization ##
    # clients "how to question" 3rd party web services like pypi, and rtd
    # making http request to web servers hosting endpoints for APIs

    # Checkers are initialized as 'Activated'
    #  if User Config is True and Default Config is False

    request.check = Engine.create(request.config_file, request.default_config)

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

    else:
        if request.config_file:
            # just update interpreters cookiecutter extra_context
            from .load_config import get_interpreters_from_yaml

            interpreters: t.Mapping[str, t.Sequence[str]] = get_interpreters_from_yaml(
                request.config_file
            )
            if interpreters:
                _context['interpreters'] = interpreters

    request.extra_context = dict(_context)
    return request
