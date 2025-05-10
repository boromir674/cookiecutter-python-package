from .helpers import parse_context
from .hosting_services import Engine


def pre_main(request):
    """Do preparatory steps before the Generation (rendering) process.

    Uses Futures to make async http request to pypi.org and readthedocs.org web
    servers to check if the "intented" project name/id is already taken.

    This is done to proactively notify the user after the Generation process
    that the project name/id is already taken, and to suggest they either change
    the project name/id or to re-run the generation process with a different
    project name/id.
    """
    ## External Services Clients Initialization ##

    # Activate: if User Config is given and Default Config is False
    deactivate_signal = request.offline or bool(request.default_config)

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

    # If INTERACTIVE, Run Interactive Dialog Pipeline, to update Context
    if interactive_mode:
        ### INTERACTIVE TERMINAL DIALOGS ###
        user_input = parse_context(request.config_file)

        ## STORE CONTEXT ##
        _context.update(
            {
                # Adapt from dialog to same interface as cookiecutter.json and biskotaki ci config file yaml
                'interpreters': {
                    'supported-interpreters': user_input.pop('supported-interpreters')
                },
                **user_input,
            }
        )

    request.extra_context = dict(_context) if _context else None
    return request
