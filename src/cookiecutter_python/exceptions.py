from cookiecutter.exceptions import (
    CookiecutterException,
    UndefinedVariableInTemplate,
)
from cookiecutter_python.backend.check_pypi import ContextVariableDoesNotExist
from cookiecutter_python.backend import CheckPypiError
from cookiecutter_python.utils import load

cookiecutter_exceptions = load(CookiecutterException, 'cookiecutter')


exceptions = {
    'critical': cookiecutter_exceptions + [ContextVariableDoesNotExist],  # type: ignore
    'non-critical': (
        CheckPypiError,
    )
}


def error_2_str(error):
    if isinstance(error, UndefinedVariableInTemplate):
        return 'non-critical'

    if isinstance(error,
        tuple(set(exceptions['critical']).difference(set([UndefinedVariableInTemplate])))
    ):
        return 'critical'
