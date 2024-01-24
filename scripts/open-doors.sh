#!/usr/bin/env sh

# Open Doors, after Release Train reaches destination

set -e

export tt='open-doors'

set +e
git tag -d "$tt"
git push --delete origin "$tt"

set -e
git tag "$tt"

git push origin "$tt"
