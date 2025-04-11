from cookiecutter_python.backend.error_handling import HandlerBuilder
from cookiecutter_python.exceptions import error_2_str


def handle_error(error):
    return HandlerBuilder.create(error_2_str(error))(error)
