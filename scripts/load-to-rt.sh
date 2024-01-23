#!/usr/bin/env sh

# Load Changes into Release Train

set -e

## Branches

# 'Release Train' git branch
RT_BRANCH="${1:-release-train}"

# branch with user's changes (ie code developed)
CHANGES_BR="${2:-$(git rev-parse --abbrev-ref HEAD)}"

MAIN_BRANCH="${3:-master}"

# 'Boarding' git branch
BRD_RT="${4:-boarding-rt}"

echo
echo "ONBOARDING Release Train: $RT_BRANCH"
echo "Changes Branch: $CHANGES_BR"

# exit if CHANGES_BR is main, master or release-train

if [ "$CHANGES_BR" = "main" ] || [ "$CHANGES_BR" = "master" ] || [ "$CHANGES_BR" = "release-train" ]; then
  echo "  [REQ]: CHANGES_BR must not be main, master or release-train!"
  echo
  echo "  [FIX]: Please checkout a different branch and re-run this script."
  echo "Exiting ..."
  exit 1
fi

# 1. push changes to topical branch of User's
git push -u origin HEAD

# Setup empemeral 'boarding-rt' branch
git checkout "$MAIN_BRANCH"
git pull origin "$MAIN_BRANCH"

set +e
git branch -D "${$BRD_RT}"
set -e

git checkout -b "${BRD_RT}"


# 2. GIT OPS

# Merge User's branch into 'boarding' to trigger Boarding CI Tests
# MERGE_MSG integrates with the .github/workflows/test.yaml workflow and
# the Test Matrix value of the STRATEGY var
MERGE_MSG="Carry User's Code, and do Boarding CI Tests"  # trigger Boarding CI Tests
# MERGE_MSG="Carry User's Code"  # skip Boarding CI Tests

git merge "${CHANGES_BR}" --no-edit --no-ff -m "${MERGE_MSG}"

# Trigger CI Tests on the 'CI/CD Pipeline'
git push -u origin HEAD

# Open PR from 'boarding' to 'release-train' branch
# and Merge MR if above CI Checks Pass
export tt='board-rt'

set +e
git tag -d "$tt"
git push --delete origin "$tt"

set -e
git tag "$tt"

git push origin "$tt"

echo
echo "GIT OPS: Tagged $tt"
echo "GIT OPS: Pushed $tt"
echo
echo "Triggered Boarding Worklow!"
echo
echo " DONE !!"

# NEXT STEPS

echo
echo " ---> NEXT STEPS:"
echo
echo "1. Go to CI: https://github.com/boromir674/cookiecutter-python-package/actions/workflows/onboard-rt.yml"


# END
echo
