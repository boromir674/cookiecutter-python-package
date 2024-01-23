#!/usr/bin/env sh

set -e

# Load Changes into Release Train

# branch with user's changes (ie code developed)
CHANGES_BR="${1:-$(git rev-parse --abbrev-ref HEAD)}"

if [ "$CHANGES_BR" = "main" ] || [ "$CHANGES_BR" = "master" ] || [ "$CHANGES_BR" = "release-train" ]; then
  echo "  [REQ]: CHANGES_BR must not be main, master or release-train!"
  echo
  echo "  [FIX]: Please checkout a different branch and re-run this script."
  echo "Exiting ..."
  exit 1
fi

git push -u origin HEAD

# GIT OPS
export tt='board-rt'

git tag "$tt" || (echo "Tag $tt already exists!" && git tag -d "$tt" && echo "Deleted local tag" && git tag "$tt" && echo "Created new tag")
git push -f origin "$tt" || (echo "Tag $tt already exists!" && git push --delete origin "$tt" && git push origin "$tt")

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
