#!/usr/bin/env sh

# NEW VERSION for Release
VERSION="${1}"

# EXAMPLE: 1.4.5

# Sem Ver Major Minor Patch + Pre-release metadata
# regex="[0-9]+\.[0-9]+\.[0-9]+(?:\-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?"


set -e


## 1. Replace Sem Ver stored in __version__ python variable of src/cookiecutter_python/__init__.py module
## 2. Replace Sem Ver mapped to 'version' field in pyproject.toml
./distro-sem-ver-bump.sh "${VERSION}"


## 3. Replace Ser Ver occurences in README.md
README_MD='README.md'
regex="[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?"

# Replace occurences such as /v2.5.8/ with /v2.5.9/
sed -i -E "s/(['\"]?v?)${regex}(['\"]?)/\1${VERSION}\2/" "${README_MD}"

# Replace occurences such as /v2.5.8..main with /v2.5.9..main
sed -i -E "s/(['\"]?v?)${regex}\.\./\1${VERSION}../" "${README_MD}"
