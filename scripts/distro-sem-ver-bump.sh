#!/usr/bin/env sh

VERSION="${1}"
GITHUB_ORG="${2:-boromir674}"
REPO="${3:-cookiecutter-python}"


# CONSTANTS
VERSION_VAR='__version__'

# DISTRO Sem Ver

## Python Poetry BUILD - Bound - Sem Ver
PYPROJECT='pyproject.toml'
sed -i -E "s/(version = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\1${VERSION}\2/" "${PYPROJECT}"

## Project Specific - Bound - Sem Ver
INIT_FILE='src/cookiecutter_python/__init__.py'
sed -i -E "s/(${VERSION_VAR} = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\1${VERSION}\2/" "${INIT_FILE}"

## Other Builds

## Python Setuptools BUILD - Bound - Sem Ver
# SETUP_PY='setup.py'
# sed -i -E "s/(version\s*=\s*['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\1${VERSION}\2/" "${SETUP_PY}"
# sed -i -E "s/(download_url\s*=\s*https:\/\/github.com\/${GITHUB_ORG}\/${REPO}\/archive\/v)[0-9]+\.[0-9]+\.[0-9]+(\.tar\.gz)/\1${VERSION}\2/" "${SETUP_PY}"

## Node BUILD - Bound - Sem Ver
# PACKAGE_JSON='package.json'
# sed -i -E "s/(\"version\": \"v?)[0-9]+\.[0-9]+\.[0-9]+(\")/\1${VERSION}\2/" "${PACKAGE_JSON}"
