
# Publish My Branch - Cheatsheet

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
function parse-version { grep -E -o '^version\s*=\s*\".*\"' pyproject.toml \| cut -d'"' -f2; }
```

From your **`User Br`** Branch:

```shell
git push
git-tag board-request
```

**Wait until** Release branch is ready and **Sync:**

```shell
git fetch && (git checkout release || git branch --track release origin/release) && git pull origin release
```
**Open PR** to `master`
```shell
./scripts/auto-release.sh
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

Clean Git with:

```shell
git checkout release && git rebase master && git push && git push origin --delete release-train
for bra in test-distro test-docs test-distro-docs boarding-auto; do git push origin -d "$bra"; done
```
