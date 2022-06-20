from cookiecutter_python.exceptions import error_2_str

from cookiecutter_python.backend.error_handling import HandlerBuilder


def handle_error(error):
    return HandlerBuilder.create(error_2_str(error))(error)
