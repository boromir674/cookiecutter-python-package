#!/usr/bin/env sh

# POSIX-compliant shell script

VERSION="${1}"


## 1. Module Specific - Sem Ver
VERSION_VAR='__version__'
INIT_FILE='src/cookiecutter_python/__init__.py'
sed -i.bak -E "s/(${VERSION_VAR} = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\\1${VERSION}\\2/" "${INIT_FILE}" && rm "${INIT_FILE}.bak"

## 2. Python Poetry BUILD - Bound - Sem Ver

# Until uv migration is verified we must update all regex matches (ie for poetry and uv config sections!)
PYPROJECT='pyproject.toml'
sed -i.bak -E "s/(version = ['\"])[0-9]+\.[0-9]+\.[0-9]+(['\"])/\\1${VERSION}\\2/" "${PYPROJECT}" && rm "${PYPROJECT}.bak"
