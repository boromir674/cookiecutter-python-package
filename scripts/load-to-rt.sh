#!/usr/bin/env sh

# Takes Changes in HEAD, and puts them on 'Release Train' (RT)

set -e

# Initialize variables
CHANGES_BR="$(git rev-parse --abbrev-ref HEAD)"
tag='board-rt'  # Default value for tag

# Process arguments
for arg in "$@"
do
    case $arg in
        # Put Changes in RT, and start RT --> Release
        --close)
            tag='auto-release'
            shift # Remove --close from processing
            ;;
        *)
            # If it's not '--close', treat it as CHANGES_BR
            CHANGES_BR="$arg"
            ;;
    esac
done

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
export tag='board-rt'

echo "[STEP]: Tag Commit: $tag"
(git tag "$tag" || (echo "* Tag $tag already exists" && git tag -d "$tag" && echo "* Deleted tag ${tag}" && git tag "$tag") && echo " -> Created tag $tag")

echo "[STEP]: Push Tag: $tag"
(git push origin --delete "$tag" && echo "* Deleted Remote tag ${tag}") || echo "* Remote Tag $tag does not exist"
git push origin "$tag" && echo " -> Pushed tag $tag"

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
