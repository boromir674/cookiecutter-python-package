#!/usr/bin/env sh

# POSIX-compliant shell script

VERSION="${1}"
GITHUB_ORG="${2:-boromir674}"
REPO="${3:-cookiecutter-python}"


# CONSTANTS
VERSION_VAR='__version__'

# FIRST we extract the semantic version string present in the sources
# VERSION_SOURCE_OF_TRUTH='src/cookiecutter_python/__init__.py'
# REGEX='^[[:space:]]*__version__[[:space:]]*=[[:space:]]*["'\'']([0-9]+)\.([0-9]+)\.([0-9]+)["'\'']'
# SEMVER="$(grep -E -o "${REGEX}" "${VERSION_SOURCE_OF_TRUTH}" | sed -E "s/${REGEX}/\1.\2.\3/")"


# # THEN we derive Release Candidate Sem Ver
# RC_SEMVER="${SEMVER}-rc"

# DISTRO Sem Ver


# Python Poetry BUILD - Bound - Sem Ver
## Until uv migration is verified we must update all regex matches (ie for poetry and uv config sections!)

PYPROJECT='pyproject.toml'
sed -i.bak -E "s/(version = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\\1${VERSION}\\2/" "${PYPROJECT}" && rm "${PYPROJECT}.bak"


## Project Specific - Bound - Sem Ver
INIT_FILE='src/cookiecutter_python/__init__.py'
sed -i.bak -E "s/(${VERSION_VAR} = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\\1${VERSION}\\2/" "${INIT_FILE}" && rm "${INIT_FILE}.bak"

## Other Builds

## Python Setuptools BUILD - Bound - Sem Ver
# SETUP_PY='setup.py'
# sed -i -E "s/(version\s*=\s*['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\1${VERSION}\2/" "${SETUP_PY}"
# sed -i -E "s/(download_url\s*=\s*https:\/\/github.com\/${GITHUB_ORG}\/${REPO}\/archive\/v)[0-9]+\.[0-9]+\.[0-9]+(\.tar\.gz)/\1${VERSION}\2/" "${SETUP_PY}"

## JS/TS / Node BUILD - Bound - Sem Ver
# PACKAGE_JSON='package.json'
# sed -i -E "s/(\"version\": \"v?)[0-9]+\.[0-9]+\.[0-9]+(\")/\1${VERSION}\2/" "${PACKAGE_JSON}"
