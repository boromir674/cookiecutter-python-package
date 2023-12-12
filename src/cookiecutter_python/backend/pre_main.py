import typing as t

from .helpers import supported_interpreters
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
    # Skipped i:
    # - User Config does not have pkg_name and, readthedocs_project_slug
    #   which are used to rderive the URLs for Future Requests
    # - checker property activate_flag is False
    """
    If skipped due to missing info in User Config, we can expect Logs roughly as:
    logger.info(
        "Skipping check of remote server, because of missing context variable"
    )
    logger.info(error)
    """

    # Case 1: NON Interactive Mode <--> `request.no_input == True`
    #   - if interpreters is None, then no user config file supplied in CLI
    # Case 2: Interactive Mode <--> `request.no_input == False`
    #   - always meaningful value, since Interactive Dialog ensures that
    interpreters: t.Optional[t.Mapping[str, t.Sequence[str]]] = supported_interpreters(
        request.config_file, request.no_input
    )
    # if None, then we are in NON interactive mode, but no User Config, passed in CLI

    if interpreters:  # update cookiecutter extra_context
        # supported interpreters supplied either from yaml or from user's input
        request.extra_context = dict(
            request.extra_context or {},
            **{
                'interpreters': interpreters,
            }
        )

    return request
