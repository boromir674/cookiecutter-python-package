#!/usr/bin/env bash

### Part of Release Process ###

# Topic_A, Topic_B, ... , Topic_N
#    \         |            /
#     \        |           /
#       \      |         /
#         \    |       /
#         Integration_Br
#              |
#          Release_Br
#              |
#          Default_Br

# RUN THIS, WHEN All changes for Release are ALREADY on the Integration_Br branch


## CONFIGURATION
### 1. SEM VER SOURCE UPDATE ###
SOURCES_TO_UPDATE='src/cookiecutter_python/__init__.py pyproject.toml uv.lock README.md'

### 2. CHANGELOG Update ###
CHANGELOG_FILE="${CHANGELOG_FILE:-CHANGELOG.md}"


# Local Constant Variables
_MAIN='master'
_DEV='dev'
RELEASE_BR='release'

# GITHUB DEFAULT_BRANCH (aka main branch)
DEFAULT_BRANCH=${_MAIN}


# INPUTS
# 1. NEW_VERSION: The new version to be released
# 2. Branch with Changes DEV (Optional): The branch where all changes for release are, initially
# 3. Branch 

# USAGE
# ./terminal-based-release.sh <NEW_VERSION> [<DEV>]
# Example:
# ./terminal-based-release.sh 0.1.0
# ./terminal-based-release.sh 0.1.0 dev

set -e

# Arguments Parsing
if [ $# -lt 1 ]; then
    echo "Usage: $0 <NEW_VERSION> [<BRANCH_WITH_CHANGES>]"
    echo
    echo "Example: $0 0.1.0"
    echo "Example: $0 0.1.0 dev"
    exit 1
fi
# New version to be released
NEW_VERSION=$1
# BRANCH WITH CHANGES WE WANT TO RELEASE to main
if [ $# -ge 2 ]; then
    BRANCH_WITH_CHANGES=$2
else
    BRANCH_WITH_CHANGES=${_DEV}
fi
# Check if the script is run from the root of the repository
if [ ! -d ".git" ]; then
    echo "This script must be run from the root of the repository."
    exit 1
fi
# Check if the user is in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "This script must be run inside a git repository."
    exit 1
fi


### MAIN SCRIPT ###

git l | head -n 10
echo "========================="
git branch -vv
echo

echo "We are about to checkout ${BRANCH_WITH_CHANGES} branch and pull latest changes !"
echo "Make sure all changes for release are already merged into ${BRANCH_WITH_CHANGES} !"
echo

read -n 1 -s -r -p "Press any key to continue .. (unless ctrl + C)"

git checkout "${BRANCH_WITH_CHANGES}"
git pull

## 1. SEM VER SOURCE UPDATE ##
echo
echo " STEP 1 ---> Automatic Sem Ver Bump in sources"
echo
bash ./scripts/sem-ver-bump.sh ${NEW_VERSION}
uv lock

git add ${SOURCES_TO_UPDATE}

echo =======
git diff --cached
echo =======
git diff --stat --cached
echo =======

# Press any key to continue dialog .. (unless ctrl + C)
read -ep "Press any key to commit!" -n1 -s

### 1.a Commit the changes
git commit -m "chore: sem ver bump to ${NEW_VERSION}"


## 2. CHANGELOG Update ##
echo
echo " STEP 2 ---> Do Heuristic CHANGELOG Auto-Update, by parsing Commits written in 'conventional' format"
. /data/repos/software-release/.env
# Do Heuristic Auto-Update, by parsing commits written in "conventional" format
release-software-rolling -cl -mb master -nv ${NEW_VERSION}

echo
echo "Read commit messages above that failed to be auto-parsed."
echo "Then do 'code ${CHANGELOG_FILE}' to manually write the Header of the new Release entry !"
echo 'Header should "talk about" the purposes/goals of the Release (why we want the changes to be released)'

# Do manual additions
read -ep "Press any key to open '${CHANGELOG_FILE}' in VS Code !" -n1 -s
code CHANGELOG.rst

read -ep "Press any key after done editing '${CHANGELOG_FILE}'" -n1 -s

git add ${CHANGELOG_FILE}
echo =======
git diff --stat --cached
echo =======

# Dialog before Commit
read -ep "Press any key to commit '${CHANGELOG_FILE}' !" -n1 -s

### 2.a Commit the changes
git commit -m "docs: add ${NEW_VERSION} Release entry in ${CHANGELOG_FILE}"

echo
echo "DONE !"

echo
read -ep "Press any key to push changes to ${BRANCH_WITH_CHANGES} remote!" -n1 -s

## PUSH Integration_Br (dev) TO REMOTE
git push

git checkout ${RELEASE_BR}
git rebase ${DEFAULT_BRANCH}
git push

git checkout "${BRANCH_WITH_CHANGES}"

## OPEN PR TO RELEASE BRANCH
gh pr create --base ${RELEASE_BR} --head "${BRANCH_WITH_CHANGES}" --title "Release v${NEW_VERSION}"


## ENABLE AUTO MERGE with 'merge' strategy (others are 'squash' and 'rebase')
# this cmd 'gh pr merge ${BRANCH_WITH_CHANGES} --merge --auto' randomly exits with error code 1.
# need to "catch" and retry untill success (max retried = 3)

set +e
gh pr merge "${BRANCH_WITH_CHANGES}" --merge --auto
if [ $? -ne 0 ]; then
    echo "gh pr merge ${BRANCH_WITH_CHANGES} --merge --auto failed, retrying..."
    for i in {1..3}; do
        gh pr merge "${BRANCH_WITH_CHANGES}" --merge --auto
        if [ $? -eq 0 ]; then
            break
        fi
    done
fi
set -e


## WATCH GITHUB ACTIONS WORKFLOWS RUNNING
echo "========== Watch GH Workflow Run =========="
gh run watch

echo "========================="
echo "DONE! PR ${BRANCH_WITH_CHANGES} --> ${RELEASE_BR} Merged !"

git checkout ${RELEASE_BR}

echo
read -ep "Press any key to update local '${RELEASE_BR}' branch from remote!" -n1 -s

## PULL RELEASE BRANCH
git pull

## CREATE PR TO DEFAULT_BRANCH (ie release --> main)
gh pr create --base ${DEFAULT_BRANCH} --head "${RELEASE_BR}" --title "Release v${NEW_VERSION}"
echo
read -ep "Press any key to make a RELEASE CANDIDATE '${RELEASE_BR}' branch from remote!" -n1 -s

## CREATE and PUSH RC TAG
RC_TAG="v${NEW_VERSION}-rc"

git tag -f "$RC_TAG"
git push origin -f "$RC_TAG"

echo
echo "Release Candidate Pipeline Triggered !"


# press any key to continue
read -ep "Please run 'gh run watch' to watch the CI/CD Pipeline (press any key to continue)" -n1 -s

# TODO: try to implement the below; currently after gh run watch finishes it stops execution of the sshell script!
# read -ep "Please watch the CI/CD Pipeline to succeed (press any key to continue to 'live watch') !" -n1 -s
# gh run watch

## PROMPT USER TO MERGE the PR if QA/CHECKS PASSED
echo "========================="
echo "Assuming CI/CD Pipeline Succeeded !"

echo "[NEXT] Please run the below to complete merge to 'main'"
echo
echo 'gh pr merge --subject "[NEW] Python Project Generator v${NEW_VERSION}" --body "Release v${NEW_VERSION}" --merge'

echo "[IF] prohibitted, you can use --admin flag:"
echo
echo 'gh pr merge --admin --subject "[NEW] Python Project Generator v${NEW_VERSION}" --body "Release v${NEW_VERSION}" --merge'

echo
# press any key to continue
read -ep "After Merge to '${DEFAULT_BRANCH}' branch is made (ie via CLI or github.com), press any key to proceed with updating local '${DEFAULT_BRANCH}' branch" -n1 -s

echo "========================="

git checkout ${DEFAULT_BRANCH}
git pull

git tag -f "v${NEW_VERSION}"
git push origin -f "v${NEW_VERSION}"
echo
echo "Release v${NEW_VERSION} is now tagged !"
echo

# press any key to continue
read -ep "Please watch the CI/CD Pipeline to succeed (press any key to continue to 'live watch') !" -n1 -s

gh run watch

# after success pypi and docker artifacts pushed !! :-)
echo
echo "========================="
echo "Release v${NEW_VERSION} is now tagged and pushed to PyPi and Docker Hub !"
echo
echo " [FINISH] :-)"