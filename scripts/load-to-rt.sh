#!/usr/bin/env sh

# Load Changes into Release Train

set -e

## Branches

# branch with user's changes (ie code developed)
CHANGES_BR="${1:-$(git rev-parse --abbrev-ref HEAD)}"

MAIN_BRANCH="${2:-master}"

# 'Boarding' git branch
BRD_RT="${3:-boarding-rt}"

echo
echo "BOARDING Branch: $BRD_RT"
echo " Changes Branch: $CHANGES_BR"
echo "    Main Branch: $MAIN_BRANCH"

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

export tt='board-rt'

git tag "$tt" || (echo "Tag $tt already exists!" && git tag -d "$tt" && git tag "$tt")
git push origin "$tt" || (echo "Tag $tt already exists!" && git push --delete origin "$tt" && git push origin "$tt")

echo
echo "Triggered Boarding Worklow!"
echo
echo " DONE !!"

# NEXT STEPS

echo
echo " ---> NEXT STEPS:"
echo
echo "1. Check CI Workflow: https://github.com/boromir674/cookiecutter-python-package/actions/workflows/load-to-rt.yml"

echo
echo "Run: ./scripts/start-rt.sh"
echo
echo "Run: ./scripts/open-doors.sh"

# END
echo
