#!/usr/bin/env sh

# NEW VERSION for Release
VERSION="${1}"
# EXAMPLE: 1.4.5

# Sem Ver Major Minor Patch + Pre-release metadata
# regex="[0-9]+\.[0-9]+\.[0-9]+(?:\-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?"

regex="[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)?"

set -e

## 1. DISTRO Sem Ver - needed for Prod tag
bash ./scripts/distro-sem-ver-bump.sh "${VERSION}"

## 2. README.md - Sem Ver
README_MD='README.md'
# sed -i -E "s/(['\"]?v?)[0-9]+\.[0-9]+\.[0-9]+(['\"]?)/\1${VERSION}\2/" "${README_MD}"

# Replace occurences such as /v2.5.8/ with /v2.5.9/
sed -i -E "s/(['\"]?v?)${regex}(['\"]?)/\1${VERSION}\2/" "${README_MD}"

# Replace occurences such as /v2.5.8..main with /v2.5.9..main
sed -i -E "s/(['\"]?v?)${regex}\.\./\1${VERSION}../" "${README_MD}"


# Sphinx Docs - Sem Ver
# DOCS_CONF='docs/conf.py'
# sed -i -E "s/(release\s*=\s*['\"]v?).+(['\"])/\1${VERSION}\2/" "${DOCS_CONF}"

### README.rst - Sem Ver
# README_RST='README.rst'

# sed -i -E "s/(['\"]?v?)[0-9]+\.[0-9]+\.[0-9]+(['\"]?)/\1${VERSION}\2/" "${README_RST}"
# sed -i -E "s/(['\"]?v)${regex}(['\"]?)/\1${VERSION}\2/" "${README_RST}"
# sed -i -E "s/(['\"]?v?)${regex}(\/|\.\.)/\1${VERSION}\2/" "${README_RST}"
# sed -i -E "s/(['\"]?v?)${regex}((\/|\.\.))/\1${VERSION}\2/g" "${README_RST}"
