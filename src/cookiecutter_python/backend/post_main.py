from requests.exceptions import ConnectionError


def post_main(request):
    for result in request.check_results:
        try:
            request.check.handle(result)
        except ConnectionError as error:
            raise CheckWebServerError(
                f"Connection error while checking {result.service_name} web server"
            ) from error


class CheckWebServerError(Exception):
    pass
