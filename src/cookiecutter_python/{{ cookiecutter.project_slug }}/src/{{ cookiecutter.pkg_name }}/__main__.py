# -*- coding: utf-8 -*-
"""Run `python -m {{ cookiecutter.pkg_name }}`.

Allow running {{ cookiecutter.project_name }}, also by invoking
the python module:

`python -m {{ cookiecutter.pkg_name }}`

This is an alternative to directly invoking the cli that uses python as the
"entrypoint".
"""
from __future__ import absolute_import

from {{ cookiecutter.pkg_name }}.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name="{{ cookiecutter.pkg_name|replace('_', '-') }}")
