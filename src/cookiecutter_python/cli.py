"""Main `cookiecutter_python` CLI."""

import os
import sys

import click

from cookiecutter_python import __version__

from .backend import generate
from .cli_handlers import handle_error
from .exceptions import exceptions


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
    u'--offline',
    is_flag=True,
    help=u'Disable Async Http Project Existence Check, on PyPI and RTD servers',
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
    offline: bool,
    checkout,
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
    try:
        project: str = generate(
            checkout=checkout,
            offline=offline,
            no_input=no_input,
            replay=replay,
            overwrite=overwrite,
            output_dir=output_dir,
            config_file=config_file,
            default_config=default_config,
            password=None,  # os.environ.get('COOKIECUTTER_REPO_PASSWORD'),
            directory=directory,
            skip_if_file_exists=skip_if_file_exists,
        )
    except exceptions['critical'] as error:
        handle_error(error)
        sys.exit(1)
    except exceptions['non-critical'] as error:
        handle_error(error)
    return project


if __name__ == "__main__":  # pragma: no cover
    main()
