
# Board Train and Release - Cheatsheet

**Requires:**
- GITHUB **Auto Merge** is ON, for Repo

*Assumes:*
- the User / Developer made all their changes on a **`User Br`** branch
- there is a dedicated **`master`** branch, for tagged production commits (public API)
- Protection Rules, with suitable Required Checks for branches
  - `master`
  - `release-train`
  - `test-distro`
  - `test-docs`
  - `test-distro-docs`

**START**

Running on **Linux shell.**

```shell
function git-tag { git tag -d "$1" || true; git tag "$1" && (git push origin -d "$1" || true); git push origin "$1"; }
function parse-version { grep -E -o '^version\s*=\s*\".*\"' pyproject.toml | cut -d'"' -f2; }
```

REPEAT for all `Topical Branches`, branching off of **`master`:**

```shell
git-tag board-request
```

EVERY topic branch should now be in **`origin/release-train`.**

```shell
git fetch
git checkout origin/release-train
git-tag start-train
```

**Wait** for **PR** *opened* **'release' --> 'master'**
- https://github.com/boromir674/cookiecutter-python-package/pulls?q=is%3Apr+is%3Aopen+base%3Amaster

```shell
git fetch && (git checkout release || git branch --track release origin/release) && git pull origin release
```
**`Sem Ver` + `Changelog`** updates on **release** branch

- [OPT1]\: For **Public API** Releases

    ```shell
    ./scripts/auto-release.sh
    ```

- [OPT2]\: For **Internal** Releases

    1. Do **Sem Ver** source updates and commits (1 or more files)
    2. Do **Changelog** update and commit (1 file)
    3. Run
        ```shell
        git push origin release
        git-tag auto-prod
        ```

1. **Code Review PR on Github**

    Go to PRs to 'master':  
    https://github.com/boromir674/cookiecutter-python-package/pulls?q=is%3Apr+is%3Aopen+base%3Amaster

Expect **PR Merge** to **`master`**, after all **Required Checks** Pass!
**Git Tag** is automatically pushed after that!

**Simply Wait** until that happens!

Now, make a **new Release:**

```shell
git checkout master && git pull && git push
export tt="v$(parse-version)"
gh release create "$tt"
```
**--> !! DONE !! <--**

Clean Origin Git with:

```shell
# Delete Git Ops TAGS
git push origin -d board-request
git push origin -d auto-prod

# Delete Git Ops BRANCHES
git push origin -d boarding-auto

git push origin -d test-docs
git push origin -d test-distro
git push origin -d test-distro-docs
git push origin -d direct-onboarding

git push origin -d release-train
git push origin -d release
```

Clean Local with:
```shell
git tag -d board-request
git tag -d auto-prod
```