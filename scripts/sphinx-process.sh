#!/usr/bin/env sh

sphinx-build -E -b doctest docs docs-dist
sphinx-build -E -b html docs docs-dist
sphinx-build -b spelling docs docs-dist
sphinx-build -b linkcheck docs docs-dist

echo "View documentation at docs-dist/index.html; it is ready to be hosted!"
