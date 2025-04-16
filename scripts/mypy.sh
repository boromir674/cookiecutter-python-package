#!/usr/bin/env sh

## Run Mypy against Code

# Env Required: .lint-env

set -e

# if env notr found exit with error
if [ ! -d .lint-env ]; then
  echo "No .lint-env found, please run 'uv venv .lint-env' first"
  exit 1
fi


# uv export --no-emit-project --no-dev --extra typing --frozen --format requirements-txt -o prod+type.txt

# . .lint-env/bin/activate

# uv pip install -r prod+type.txt

# set mypy environment
export MYPYPATH=${MYPYPATH:-src/stubs}

# DRYness
PKG=${PGK:-src/cookiecutter_python}

mypy --show-error-codes --check-untyped-defs \
    --exclude tests/data \
    "${PKG}/hooks" \
    "${PKG}/backend" "${PKG}/handle" \
    "${PKG}/utils.py" "${PKG}/exceptions.py" \
    "${PKG}/cli.py" "${PKG}/cli_handlers.py" \
    "${PKG}/__main__.py" "${PKG}/__init__.py" \
    tests
