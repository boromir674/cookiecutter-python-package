from cookiecutter.exceptions import (
    CookiecutterException,
    UndefinedVariableInTemplate,
)
from cookiecutter_python.backend.hosting_services.exceptions import ContextVariableDoesNotExist
from cookiecutter_python.backend import CheckWebServerError
from cookiecutter_python.utils import load

cookiecutter_exceptions = load(CookiecutterException, 'cookiecutter')


exceptions = {
    'critical': tuple(cookiecutter_exceptions + [ContextVariableDoesNotExist]),  # type: ignore
    'non-critical': (
        CheckWebServerError,
    )
}


def error_2_str(error):
    if isinstance(error, UndefinedVariableInTemplate):
        return 'non-critical'

    if isinstance(error,
        tuple(set(exceptions['critical']).difference(set([UndefinedVariableInTemplate])))
    ):
        return 'critical'
