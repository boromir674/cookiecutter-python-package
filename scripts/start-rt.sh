#!/usr/bin/env sh

# Prepare Release Train
# Eg: create a release-candidate, do a pre-release, stress testing, etc

set -e

RC_TEST=true

RW_BIN="${1:-release-software-rolling}"

## Branches

# 'Release Train' git branch
RT_BRANCH="${2:-release-train}"

MAIN_BRANCH="${3:-master}"

RELEASE_BRANCH="${4:-release}"

echo

echo "PREPARING for Release.."
echo

git fetch
git checkout "$MAIN_BRANCH"
git pull origin "$MAIN_BRANCH"

# Setup Release Branch to Point to Main/Master
git branch -f "$RELEASE_BRANCH" HEAD || git checkout -b "$RELEASE_BRANCH"

# Merge Release Train into Release Branch
git merge "$RT_BRANCH" --no-ff

# Update Sem Ver and Changelog, and commit
$RW_BIN -c release.yml


if [[ "$RC_TEST" = true ]]; then
  echo
  echo "Stress Testing Release.."
  
  # append '-rc' to end of `__version__ = ['"]M.m.p["']` in __init__.py
  sed -i -E 's/(__version__ = ['"'"'][0-9]+\.[0-9]+\.[0-9]+)('"'"'])/\1-rc\2/' src/cookiecutter_python_package/__init__.py
  
  # append '-rc' to end of `version = ['"]M.m.p["']` in pyproject.toml
  sed -i -E 's/(version = ['"'"'][0-9]+\.[0-9]+\.[0-9]+)('"'"'])/\1-rc\2/' pyproject.toml

  echo
  git status -uno

  echo
  RC_MSG="chore(semver): add -rc (release candidate) to Source and Distro versions"
  git add -u
  git commit -m "$RC_MSG"
  
  commit_sha=$(git rev-parse HEAD)

  echo

  ###### GIT OPS ######
  rc_tag="v$(./scripts/parse_version.py)-rc"

  export tt="${rc_tag}"

  echo "[STEP]: Tag Commit: $tt"
  (git tag "$tt" || (echo "* Tag $tt already exists" && git tag -d "$tt" && echo "* Deleted tag ${tt}" && git tag "$tt") && echo " -> Created tag $tt")

  ### TRIGGER RELEASE CANDIDATE - TESTS ###
  echo "[STEP]: Push Tag: $tt"
  (git push origin --delete "$tt" && echo "* Deleted Remote tag ${tt}") || echo "* Remote Tag $tt does not exist"
  git push origin "$tt" && echo " -> Pushed tag $tt"

  ### Revert to Production Sem Ver ###
  git revert "$commit_sha" --no-commit
  git commit -m "revert: $RC_MSG\n\nThis reverts commit $commit_sha."
fi

# Update Release Upstream Branch
git push -u origin HEAD


echo
echo " DONE !!"

# NEXT STEPS

echo
echo " ---> NEXT STEPS:"
echo
echo "1. Go to CI: https://github.com/boromir674/cookiecutter-python-package/actions/workflows/test.yml"

echo "2. Validate Release Candidate Passed all QA"
echo "  Eg: Check CI stress Tests, rtd integration, etc"

echo
echo "3. Run ./scripts/open-doors.sh"

# END
echo
