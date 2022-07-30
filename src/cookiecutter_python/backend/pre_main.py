from .context import create_context
from .helpers import supported_interpreters
from .hosting_services import Engine
from .request import Request


def pre_main(**kwargs):
    request = Request(**kwargs)

    request.check = Engine.create(request.config_file, request.default_config)

    request.check_results = request.check.check(request.web_servers)

    interpreters = supported_interpreters(request.config_file, request.no_input)
    if interpreters:  # update extra_context
        # supported interpreters supplied either from yaml or from user's input
        request.extra_context = create_context(
            interpreters, extra_context=request.extra_context
        )
    return request
