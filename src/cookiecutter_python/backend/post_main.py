from requests.exceptions import ConnectionError as RequestsConnectionError


def post_main(request):
    """Check if any CI 'deployment' (ie in pypi), would require minor tweak."""
    # ie if gen proj py pkg name is 'gg', and pypi.org/project/gg/ is already taken
    for result in request.check_results:
        try:
            request.check.handle(result)
        except RequestsConnectionError as error:
            raise CheckWebServerError(
                f"Connection error while checking {result.service_name} web server"
            ) from error


class CheckWebServerError(Exception):
    """Raised on Connection Error, when Requesting a Web Server's Future."""

    pass
