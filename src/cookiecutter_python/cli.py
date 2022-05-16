# -*- coding: utf-8 -*-

"""Main `cookiecutter_python` CLI."""

import json
import os
import sys

import click
from cookiecutter.exceptions import (
    FailedHookException,
    InvalidModeException,
    InvalidZipRepository,
    OutputDirExistsException,
    RepositoryCloneFailed,
    RepositoryNotFound,
    UndefinedVariableInTemplate,
    UnknownExtension,
)

from cookiecutter_python import __version__
from cookiecutter_python.backend.check_pypi import ContextVariableDoesNotExist
from cookiecutter_python.backend.main import CheckPypiError, generate

this_file_location = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))


def version_msg():
    """Message about Python Generator version, location and Python version."""
    python_version = sys.version[:3]
    message = u'Python Generator %(version)s from {} (Python {})'
    location = os.path.dirname(this_file_location)
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'--version', message=version_msg())
@click.option(
    u'--no-input',
    is_flag=True,
    help=u'Do not prompt for parameters and only use cookiecutter.json ' u'file content',
)
@click.option(
    u'-c',
    u'--checkout',
    help=u'branch, tag or commit to checkout after git clone',
)
@click.option(
    u'--directory',
    help=u'Directory within repo that holds cookiecutter.json file '
    u'for advanced repositories with multi templates in it',
)
@click.option('-v', '--verbose', is_flag=True, help='Print debug information', default=False)
@click.option(
    u'--replay',
    is_flag=True,
    help=u'Do not prompt for parameters and only use information entered ' u'previously',
)
@click.option(
    u'-f',
    u'--overwrite',
    is_flag=True,
    help=u'Overwrite the contents of the output directory if it already exists',
)
@click.option(
    u'-s',
    u'--skip-if-file-exists',
    is_flag=True,
    help=u'Skip the files in the corresponding directories if they already ' u'exist',
    default=False,
)
@click.option(
    u'-o',
    u'--output-dir',
    default='.',
    type=click.Path(),
    help=u'Where to output the generated project dir into',
)
@click.option(
    u'--config-file', type=click.Path(), default=None, help=u'User configuration file'
)
@click.option(
    u'--default-config',
    is_flag=True,
    help=u'Do not load a config file. Use the defaults instead',
)
def main(
    no_input,
    checkout,
    verbose,
    replay,
    overwrite,
    output_dir,
    config_file,
    default_config,
    directory,
    skip_if_file_exists,
):
    """Create a Project from the project template.

    Cookiecutter Python Package is Free/Libre Open Source Software. If you would
    like to get in touch, please see
    https://github.com/boromir674/cookiecutter-python-package.
    """

    # TODO Improvement: add logging configuration
    # from cookiecutter.log import configure_logger
    # configure_logger(stream_level='DEBUG' if verbose else 'INFO', debug_file=debug_file)

    try:
        project: str = generate(
            checkout,
            no_input,
            replay=replay,
            overwrite=overwrite,
            output_dir=output_dir,
            config_file=config_file,
            default_config=default_config,
            password=None,  # os.environ.get('COOKIECUTTER_REPO_PASSWORD'),
            directory=directory,
            skip_if_file_exists=skip_if_file_exists,
        )
    except CheckPypiError as error:
        click.echo(error)
    except (  # cookiecutter exceptions
        OutputDirExistsException,
        InvalidModeException,
        FailedHookException,
        UnknownExtension,
        InvalidZipRepository,
        RepositoryNotFound,
        RepositoryCloneFailed,
        # python generator exceptions
        ContextVariableDoesNotExist,
    ) as error:
        click.echo(error)
        sys.exit(1)
    except UndefinedVariableInTemplate as undefined_err:
        click.echo('{}'.format(undefined_err.message))
        click.echo('Error message: {}'.format(undefined_err.error.message))

        context_str = json.dumps(undefined_err.context, indent=4, sort_keys=True)
        click.echo('Context: {}'.format(context_str))
        sys.exit(1)
    return project


if __name__ == "__main__":  # pragma: no cover
    main()
