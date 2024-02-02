"""Run `python -m biskotakigold`.

Allow running Biskotaki Gold Standard, also by invoking
the python module:

`python -m biskotakigold`

This is an alternative to directly invoking the cli that uses python as the
"entrypoint".
"""

from __future__ import absolute_import

from biskotakigold.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name="biskotakigold")
