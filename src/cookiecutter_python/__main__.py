# -*- coding: utf-8 -*-
"""Allow python generator to be executable through `python -m generate-python`."""
from __future__ import absolute_import

from cookiecutter_python.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name='generate-python')
