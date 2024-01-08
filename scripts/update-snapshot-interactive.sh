#!/usr/bin/env sh

# Update the Snashot Biskotaki (ci) Test Data maintained for
# Regression Tests

set -e
export TOXPYTHON=python3.10
# From 'edit' mode installation:
echo
tox -e dev -vv --notest

set +e
rm -rf /tmp/biskotaki
set -e

### RUN Generator in Interactive Mode, prompting/asking for user input ###
echo
.tox/dev/bin/generate-python --config-file .github/biskotaki.yaml -o /tmp/

### UPDATE SNAPSHOT, by Copying all Generated files and folders recursively ###
INTERACTIVE_SNAPSHOT=${INTERACTIVE_SNAPSHOT:-tests/data/snapshots/biskotaki-interactive}

set +e
rm -rf "${INTERACTIVE_SNAPSHOT}"
set -e
# copy generated biskotaki to 'biskotaki-no-input' test Snapshot
cp -r /tmp/biskotaki/ "${INTERACTIVE_SNAPSHOT}"


# show diff of biskotaki-interactive
echo
git diff --stat "${INTERACTIVE_SNAPSHOT}"

# get only last part of path from NO_INPUT_SNAPSHOT
INTERACTIVE_SNAPSHOT_NAME=$(echo "${INTERACTIVE_SNAPSHOT}" | awk -F/ '{print $NF}')

echo
echo "Next steps:"
echo
echo "git add ${INTERACTIVE_SNAPSHOT}"
echo "git commit -m \"tests(data): update ${INTERACTIVE_SNAPSHOT_NAME} Snapshot, used in Regression Testing\""
echo

## GIT ADD ##
# git add "${INTERACTIVE_SNAPSHOT}"
# echo

## GIT COMMIT ##
# git cz
# echo
# echo "Snapshot updated!"