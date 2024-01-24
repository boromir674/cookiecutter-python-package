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

echo "[STEP]: Ensure Upstream is up-to-date with User's Branch"
git push -u origin HEAD

# GIT OPS
export tt='board-rt'

echo "[STEP]: Tag Commit: $tt"
(git tag "$tt" || (echo "[INFO] Tag $tt already exists" && git tag -d "$tt" && echo "[INFO] Deleted tag ${tt}" && git tag "$tt") && echo " -> Tagged with $tt")

echo "[STEP]: Push Tag: $tt"
(git push origin --delete "$tt" && echo "* Deleted Remote tag ${tt}") || echo "* Remote Tag $tt does not exist"
git push origin "$tt" && echo " -> Pushed tag $tt"

echo
echo " DONE !!"
echo
echo " Triggered Boarding Worklow!"

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
