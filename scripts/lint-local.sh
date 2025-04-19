#!/usr/bin/env sh

# Run Linters and modify in place !

set -e


# find all .yml or .yaml files in template dir and verify valid yaml

SEARCH_DIR='tests/data/snapshots/'


echo DONE

# V2 for any posix-compliant shell
find "${SEARCH_DIR}" -type f \( -name "*.yml" -o -name "*.yaml" \) | while read yaml_file; do
  if [ ! -f "$yaml_file" ]; then
    echo "ERROR: $yaml_file does not exist"
    exit 1
  fi

  # Check if the file is a valid YAML file
  if ! yq eval '.' "$yaml_file" > /dev/null 2>&1; then
    echo "ERROR: $yaml_file is not a valid YAML file"
    exit 1
  fi
done


# Require Clean Git Working Dir Status

if [ -n "$(git status --porcelain -uno)" ]; then
  echo "Git Working Directory is not clean!"
  echo "Please commit or stash your changes before running this script."
  exit 1
fi

LINT_EXCLUDE='tests/data/snapshots'
LINT_ARGS="src tests scripts"

uv venv .lint-env
. .lint-env/bin/activate
uv pip install 'isort>=5.12.0, <6.0.0' 'black>=23.3.0, <24.0.0' 'ruff' 'prospector[with_pyroma]'

## APPLY ISORT ##
  # --skip tests/data/snapshots \
echo "[INFO] Running Isort..."
uv run --active isort \
  --skip 'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' \
  ${LINT_ARGS}


# if files changed (git diff), then add and commit
if [ -n "$(git status --porcelain -uno)" ]; then
  git add -u
  git commit -m "refactor(isort): apply isort"
fi

  # --exclude tests/data/snapshots \
## APPLY BLACK ##
echo "[INFO] Running Black..."
uv run --active black \
  --skip-string-normalization \
  --extend-exclude 'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' \
  --config pyproject.toml \
  ${LINT_ARGS}


# if files changed (git diff), then add and commit
if [ -n "$(git status --porcelain -uno)" ]; then
  git add -u
  git commit -m "refactor(black): apply black"
fi

## APPLY RUFF ##
echo "[INFO] Running Ruff..."
uv run --active ruff check --fix \
  --extend-exclude 'src/cookiecutter_python/\{\{\ cookiecutter.project_slug\ \}\}' \
  ${LINT_ARGS}

# if files changed (git diff), then add and commit
if [ -n "$(git status --porcelain -uno)" ]; then
  git add -u
  git commit -m "refactor(ruff): apply ruff"
fi

set +e

uv run --active isort --check --skip tests/data/snapshots --skip 'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' ${LINT_ARGS}
uv run --active black --check --skip-string-normalization --exclude tests/data/snapshots --extend-exclude 'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' --config pyproject.toml ${LINT_ARGS}
uv run --active ruff check --extend-exclude 'src/cookiecutter_python/\{\{\ cookiecutter.project_slug\ \}\}' ${LINT_ARGS}

uv run --active prospector src
uv run --active prospector tests

set -e

echo
echo " ---> Linters applied !!"
echo
echo "For Final Sanity, run:"
echo
# echo "tox -e isort && tox -e black && tox -e ruff && tox -e prospector && tox -e pin-deps -- -E typing && tox -e type"
echo ". .lint-env/bin/activate && export LINT_EXCLUDE='tests/data/snapshots' && export LINT_ARGS='src tests scripts' && uv run --active isort --check --skip tests/data/snapshots --skip 'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' ${LINT_ARGS} && uv run --active black --check --skip-string-normalization --exclude tests/data/snapshots --extend-exclude 'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' --config pyproject.toml ${LINT_ARGS} && uv run --active ruff check --extend-exclude 'src/cookiecutter_python/\{\{\ cookiecutter.project_slug\ \}\}' ${LINT_ARGS} && uv run --active prospector src && uv run --active prospector tests"
echo
