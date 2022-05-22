# -*- coding: utf-8 -*-
"""Allow to run Python Generator also through `python -m cookiecutter_python`.

Allows Python Generator to be executed through `python -m cookiecutter_python`.
"""
from __future__ import absolute_import

from cookiecutter_python.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name='generate-python')
