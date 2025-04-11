"""Main `{{ cookiecutter.pkg_name }}` CLI."""

import os
import sys

import click

from . import __version__


this_file_location = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))


def version_msg():
    """{{ cookiecutter.pkg_name }} version, location and Python version.

    Get message about {{ cookiecutter.pkg_name }} version, location
    and Python version.
    """
    python_version = sys.version[:3]
    message = u"{{ cookiecutter.project_name }} %(version)s from {} (Python {})"
    location = os.path.dirname(this_file_location)
    return message.format(location, python_version)


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'--version', message=version_msg())
# @click.option('-v', '--verbose', is_flag=True, help='Print debug information', default=False)
def main(
    # verbose,
):
    """TODO Write this content that gets renders when invoking with --help flag!"""
    try:
        pass
    except Exception as error:  # pylint: disable=broad-except
        click.echo(error)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
