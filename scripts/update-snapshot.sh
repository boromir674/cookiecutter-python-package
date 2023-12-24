#!/usr/bin/env sh

# Update the Snashot Biskotaki (ci) Test Data maintained for Regression Tests

set -e
export TOXPYTHON=python3.10
# From 'edit' mode installation:
echo
tox -e dev -vv --notest

set +e
rm -rf /tmp/biskotaki
set -e

### RUN Generator in Non-Interactive Mode ###
echo
.tox/dev/bin/generate-python --no-input --config-file .github/biskotaki.yaml -o /tmp/


### UPDATE SNAPSHOT, by Copying all Generated files and folders recursively ###
NO_INPUT_SNAPSHOT=${NO_INPUT_SNAPSHOT:-tests/data/snapshots/biskotaki-no-input}
set +e
rm -rf "${NO_INPUT_SNAPSHOT}"
set -e
# copy generated biskotaki to 'biskotaki-no-input' test Snapshot
cp -r /tmp/biskotaki/ "${NO_INPUT_SNAPSHOT}"


# show diff of biskotaki-no-input
echo
git diff --stat "${NO_INPUT_SNAPSHOT}"

# get only last part of path from NO_INPUT_SNAPSHOT
NO_INPUT_SNAPSHOT_NAME=$(echo "${NO_INPUT_SNAPSHOT}" | awk -F/ '{print $NF}')


echo
echo "Next steps:"
echo
echo "git add ${NO_INPUT_SNAPSHOT}"
echo "git commit -m \"tests(data): update ${NO_INPUT_SNAPSHOT_NAME} Snapshot, used in Regression Testing\""
echo

## GIT ADD ##
# git add "${NO_INPUT_SNAPSHOT}"
# echo

## GIT COMMIT ##
# git cz
# echo
# echo "Snapshot updated!"
