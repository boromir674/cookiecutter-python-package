#!/usr/bin/env sh

# NEW VERSION for Release
VERSION="${1}"

# EXAMPLE: 1.4.5

# Sem Ver Major Minor Patch + Pre-release metadata
# regex="[0-9]+\.[0-9]+\.[0-9]+(?:\-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?"


set -e


## 1. Replace Sem Ver stored in __version__ python variable of src/cookiecutter_python/__init__.py module
VERSION_VAR='__version__'
INIT_FILE='src/cookiecutter_python/__init__.py'
sed -i.bak -E "s/(${VERSION_VAR} = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\\1${VERSION}\\2/" "${INIT_FILE}" && rm "${INIT_FILE}.bak"


## 2. Replace Sem Ver mapped to 'version' field in pyproject.toml

# Until uv migration is verified we must update all regex matches (ie for poetry and uv config sections!)
PYPROJECT='pyproject.toml'
sed -i.bak -E "s/(version = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\\1${VERSION}\\2/" "${PYPROJECT}" && rm "${PYPROJECT}.bak"


## 3. Replace Ser Ver occurences in README.md
README_MD='README.md'
regex="[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?"

# Replace occurences such as /v2.5.8/ with /v2.5.9/
sed -i -E "s/(['\"]?v?)${regex}(['\"]?)/\1${VERSION}\2/" "${README_MD}"

# Replace occurences such as /v2.5.8..main with /v2.5.9..main
sed -i -E "s/(['\"]?v?)${regex}\.\./\1${VERSION}../" "${README_MD}"
