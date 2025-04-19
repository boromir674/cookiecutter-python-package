import typing as t

from cookiecutter.exceptions import CookiecutterException, UndefinedVariableInTemplate

from cookiecutter_python.backend import CheckWebServerError
from cookiecutter_python.backend.hosting_services.exceptions import (
    ContextVariableDoesNotExist,
)
from cookiecutter_python.utils import load


cookiecutter_exceptions = load(CookiecutterException, 'cookiecutter')


exceptions: t.MutableMapping[str, t.Tuple[t.Type[Exception], ...]] = {
    'critical': tuple(cookiecutter_exceptions + [ContextVariableDoesNotExist]),  # type: ignore
    'non-critical': (CheckWebServerError,),
}


def error_2_str(error):
    recognized_non_critical = {UndefinedVariableInTemplate}
    recognized_critical = set(exceptions['critical']).difference(recognized_non_critical)

    ## Mark NON Critical for program execution ##
    # Program should potentially be able to handle that exception and proceed
    if isinstance(error, tuple(recognized_non_critical)):
        # We 'mark as non-critical', when we find out-of-scope variables (when a
        # template uses a variable which is not defined in the context),
        # anticipating the injection of out-of-scope variables programmatically.
        return 'non-critical'

    ## Mark CRITICAL for program execution ##
    # Program's execution should potentially stop, as unable to handle exception
    if isinstance(error, tuple(recognized_critical)):
        # We Classify as Critical, all our Generator's backend engine Exceptions
        # which are cokiecutter exceptions, but we exclude
        # UndefinedVariableInTemplate and we add our Generator's exceptions:
        # - ContextVariableDoesNotExist
        return 'critical'
