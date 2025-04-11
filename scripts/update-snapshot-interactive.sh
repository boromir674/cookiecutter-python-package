#!/usr/bin/env sh

# Update the Snashot Biskotaki (ci) Test Data maintained for
# Regression Tests

set -e

# From 'edit' mode installation:
echo
tox -e dev -vv --notest

set +e
rm -rf /tmp/biskotaki
set -e

### RUN Generator in Interactive Mode, prompting/asking for user input ###
echo
.tox/dev/bin/generate-python --offline --config-file .github/biskotaki.yaml -o /tmp/

### UPDATE SHAPSHOT, by Copying all Generated files and folders recursively ###
INTERACTIVE_SHAPSHOT=${INTERACTIVE_SHAPSHOT:-tests/data/snapshots/biskotaki-interactive}

set +e
rm -rf "${INTERACTIVE_SHAPSHOT}"
set -e
# copy generated biskotaki to 'biskotaki-no-input' test Snapshot
cp -r /tmp/biskotaki/ "${INTERACTIVE_SHAPSHOT}"


# show diff of biskotaki-interactive
echo
git diff --stat "${INTERACTIVE_SHAPSHOT}"

# get only last part of path from NO_INPUT_SHAPSHOT
INTERACTIVE_SHAPSHOT_NAME=$(echo "${INTERACTIVE_SHAPSHOT}" | awk -F/ '{print $NF}')

echo
echo "Next steps:"
echo
echo "git add ${INTERACTIVE_SHAPSHOT}"
echo "git commit -m \"tests(data): update ${INTERACTIVE_SHAPSHOT_NAME} Snapshot, used in Regression Testing\""
echo

## GIT ADD ##
# git add "${INTERACTIVE_SHAPSHOT}"
# echo

## GIT COMMIT ##
# git cz
# echo
# echo "Snapshot updated!"