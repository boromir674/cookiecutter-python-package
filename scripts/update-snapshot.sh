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


### UPDATE SHAPSHOT, by Copying all Generated files and folders recursively ###
NO_INPUT_SHAPSHOT=${NO_INPUT_SHAPSHOT:-tests/data/snapshots/biskotaki-no-input}
set +e
rm -rf "${NO_INPUT_SHAPSHOT}"
set -e
# copy generated biskotaki to 'biskotaki-no-input' test Snapshot
cp -r /tmp/biskotaki/ "${NO_INPUT_SHAPSHOT}"


# show diff of biskotaki-no-input
echo
git diff --stat "${NO_INPUT_SHAPSHOT}"

# get only last part of path from NO_INPUT_SHAPSHOT
NO_INPUT_SHAPSHOT_NAME=$(echo "${NO_INPUT_SHAPSHOT}" | awk -F/ '{print $NF}')


echo
echo "Next steps:"
echo
echo "git add ${NO_INPUT_SHAPSHOT}"
echo "git commit -m \"tests(data): update ${NO_INPUT_SHAPSHOT_NAME} Snapshot, used in Regression Testing\""
echo

## GIT ADD ##
# git add "${NO_INPUT_SHAPSHOT}"
# echo

## GIT COMMIT ##
# git cz
# echo
# echo "Snapshot updated!"
