#!/usr/bin/env bash

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

# UPDATE Master/Main
# git checkout "$MAIN_BRANCH"
# git pull origin "$MAIN_BRANCH"

# # UPDATE Release Train
# git branch --track "$RT_BRANCH" "origin/${RT_BRANCH}" || echo "* Branch $RT_BRANCH already exists"
# git checkout "$RT_BRANCH"
# git pull

# Setup Release Branch to Point to Main/Master
UPSTREAM_RELEASE=$(git ls-remote --heads origin "${RELEASE_BRANCH}")

if [[ -z "${UPSTREAM_RELEASE}" ]]; then
  echo "* Upstream '${UPSTREAM_RELEASE}' does not exist"
  if [[ -n $(git branch --list "${RELEASE_BRANCH}") ]]; then
    echo "* Local '${RELEASE_BRANCH}' exists"
    # CHECKOUT
    git checkout "$RELEASE_BRANCH"
  else
    echo "* Local '${RELEASE_BRANCH}' does not exist"
    # CHECKOUT -b
    git checkout -b "$RELEASE_BRANCH"
  fi
else  # pull or track remote and checkout
  echo "* Upstream '${UPSTREAM_RELEASE}' exists"
  if [[ -n $(git branch --list "${RELEASE_BRANCH}") ]]; then
    echo "* Local '${RELEASE_BRANCH}' exists"
    git checkout "$RELEASE_BRANCH"
    # PULL Remote
    git pull origin "$RELEASE_BRANCH"
  else
    echo "* Local '${RELEASE_BRANCH}' does not exist"
    # TRACK Upstream and CHECKOUT
    git branch --track "$RELEASE_BRANCH" "origin/${RELEASE_BRANCH}"
    git checkout "$RELEASE_BRANCH"
  fi 
fi

# REBASE 'Release' on 'Master/Main'
echo "[STEP]: Rebase 'Release' on top of 'Master/Main'"
git rebase "$MAIN_BRANCH"
# Local Release branch is ready

# MERGE 'Release Train' into 'Release'
echo "[STEP]: Merge 'Release Train' into 'Release'"
git merge "$RT_BRANCH" --no-ff --no-edit

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
  
  # Local Release branch is ready for RC Test/Release

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

echo "[STEP]: Push 'Release' to Remote"
git push origin "$RELEASE_BRANCH"
# Upstream Release branch is ready for Prod Release

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
