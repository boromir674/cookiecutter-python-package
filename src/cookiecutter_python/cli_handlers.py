import json
import click

from cookiecutter.exceptions import (
    FailedHookException,
    InvalidModeException,
    InvalidZipRepository,
    OutputDirExistsException,
    RepositoryCloneFailed,
    RepositoryNotFound,
    UnknownExtension,
    UndefinedVariableInTemplate,
)
from cookiecutter_python.backend.check_pypi import ContextVariableDoesNotExist
from .backend import CheckPypiError

exceptions = {
    'critical': (
        FailedHookException,
        InvalidModeException,
        InvalidZipRepository,
        OutputDirExistsException,
        RepositoryCloneFailed,
        RepositoryNotFound,
        UnknownExtension,
        UndefinedVariableInTemplate,
        ContextVariableDoesNotExist,
    ),
    'non-critical': (
        CheckPypiError,
    )
}

# error/exception handlers

def print_error(error):
    click.echo(error)


def handle_context_error(error):
    click.echo('{}'.format(error.message))
    click.echo('Error message: {}'.format(error.error.message))

    context_str = json.dumps(error.context, indent=4, sort_keys=True)
    click.echo('Context: {}'.format(context_str))


def handle_error(error):
    if isinstance(error,
        tuple(set(exceptions['critical']).difference(set([UndefinedVariableInTemplate])))
    ):
        return print_error(error)
    if isinstance(error, UndefinedVariableInTemplate):
        return handle_context_error(error)
