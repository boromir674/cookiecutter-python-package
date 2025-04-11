
# GIT OPS

Git Ops Framework facilitating (semi) automated flows:
- `Publish my branch`

### Dev Environment - Setup

| Expression | Description | Example | Idea |
| ---------- | ----------- | ------- | ---- |
| `alias git-tag="${PWD}/scripts/git-tag.sh"` | **Tag HEAD**, *local* and *remote* | `git-tag auto-release` | Facilitates Git-Ops, given input tag |
| `function git-tag { git tag -d "$1"; git tag "$1" && git push origin -d "$1"; git push origin "$1"; }` | **Tag HEAD**, *local* and *remote* | `git-tag auto-release` | Facilitates Git-Ops, given input tag |
| `function parse-version { grep -E -o '^version\s*=\s*\".*\"' pyproject.toml \| cut -d'"' -f2; }` | **Parse Version** from pyproject.toml | `parse-version` | Query Single Source of Truth |

### Github - setup

There multiple phases of the porcess where we want to achieve behaviour such as:
- `Merge Branch A to Branch B`, after its corresponding PR's `Required Checks` **Pass**.

We leverage Github `Branch Protection Rules`, while timely enabling `Auto Merge` on github PRs, to achieve such behaviour.

We expect `Protection Rules` to be in place for below Branches:

- `master`
- `release-train`
- `test-distro`
- `test-docs`
- `test-distro-docs`

#### **How-to**: enable `Auto Merge` for your github repo

1. Navigate to the `General` Repo settings on github.com
   **Go to** https://github.com/boromir674/cookiecutter-python-package/settings and **enable checkbox** `Allow auto-merge`, as shown in the sample github screenshot, below:  
   ![Alt text](./gh-web-ui-allow_auto-merge.png)

## Publish my Branch - Flow

Here you can find the definition of `Publish my Branch` Flow and `How-to` guides.  


### Definition of `Publish my Branch` Flow

The **`Publish my Branch`** Flow is a **process**, where the **User changes** are
shipped / released to `production`.

**Assumptions:**
- the User / Developer made all their changes on a **`User Br`** branch
- there is a dedicated **`main / master`** branch, for tagged production commits (public API)

Thus, a starting git state should look like below:

<!-- 'theme': 'base',  -->


```{mermaid}
    %%{init: { 'logLevel': 'debug', 'gitGraph': {'showBranches': true, 'showCommitLabel':true,'mainBranchName': 'main / master'}} }%%

    gitGraph
        commit id: "[NEW] Gen 1.2.0" type: HIGHLIGHT tag: "v1.2.0"
        commit id: "[NEW] Gen 1.2.1" type: HIGHLIGHT tag: "v1.2.1"
        commit id: "[NEW] Gen 1.3.0" type: HIGHLIGHT tag: "v1.3.0"
        branch "User Br"
        commit
        commit id: "new feat"
```

### **How-to:** initiate the `Publish my Branch` Flow
Assuming Github and Dev Environment, are properly setup.

1. **Run in terminal**
    
    ```shell
    git push
    git-tag board-request
    ```

    This should **Automatically Trigger** the **`pr-to-boarding` Workflow**, which:
    
      1. **Opens PR** from `User Branch` to `boarding-auto`
      2. **Labels** PR, based on files changed
      3. **Labels** PR, for `Auto Merge` into **`Train`**
      4. **Merges PR** `User Branch`  -->   `boarding-auto`
      5. **Opens PR** `boarding-auto` --> `release-train`, and **merge** if *PR OK*
      6. **Opens PR** `release-train` --> `release`, and **merge** if *PR OK*

            ```{mermaid}

            %%{init: { 'logLevel': 'debug', 'theme': 'default', 'gitGraph': {'rotateCommitLabel': false, 'showBranches': true, 'showCommitLabel':true, 'mainBranchName': 'main / master'}} }%%
                gitGraph
                    commit id: "1.2.0" type: HIGHLIGHT tag: "v1.2.0"
                    commit id: "1.2.1" type: HIGHLIGHT tag: "v1.2.1"
                    commit id: "1.3.0" type: HIGHLIGHT tag: "v1.3.0"

                    branch release
                    branch release-train
                    branch "Protected Branch"
                    branch boarding-auto
                    branch "User Br"

                    commit
                    commit id: "new feat"

                    checkout boarding-auto
                    merge "User Br" id: "Classify Type of Changes"

                    checkout "Protected Branch"
                    merge "boarding-auto" id: "Accept User changes"

                    checkout release-train
                    merge "Protected Branch" id: "Integrate into Train"

                    checkout release
                    merge release-train id: "Start Release"
            ```



    So now, the `release` branch is updated on the remote,  


2. Now, sync your `release` local branch, by **running:**
    ```shell
    git fetch && (git checkout release || git branch --track release origin/release) && git pull origin release
    ```

3. **Run interactive script**

    NOTE: This assumes a `Prod` Release ie from 1.2.3 to 1.2.4 and NOT a `Dev`, ie 1.2.4-dev
    ```shell
    ./scripts/auto-release.sh
    ```

    This should:
      1. `Ask` for new *Release Sem Ver*
      2. `Ask` user to *Update Changelog themselves*
      3. `Trigger` *Distro Release* CI Tests, with *Job Matrix*
      4. `PR` 'release' --> 'master', and merge if *PR OK*

            ```{mermaid}

            %%{init: { 'logLevel': 'debug', 'theme': 'default', 'gitGraph': {'showBranches': true, 'showCommitLabel':true, 'mainBranchName': 'main / master'}} }%%
                gitGraph
                    commit id: "1.2.0" type: HIGHLIGHT tag: "v1.2.0"
                    commit id: "1.2.1" type: HIGHLIGHT tag: "v1.2.1"
                    commit id: "1.3.0" type: HIGHLIGHT tag: "v1.3.0"

                    branch release
                    branch release-train
                    branch "Protected Branch"
                    branch boarding-auto
                    branch "User Br"

                    commit
                    commit id: "new feat"

                    checkout boarding-auto
                    merge "User Br" id: "Classify Changes" type: HIGHLIGHT

                    checkout "Protected Branch"
                    merge "boarding-auto" id: "Accept User changes" type: HIGHLIGHT

                    checkout release-train
                    merge "Protected Branch" id: "Integration Tests" type: HIGHLIGHT

                    checkout release
                    merge release-train id: "Start Release" type: HIGHLIGHT

                    commit id: "Sem Ver PROD"
                    commit id: "Changelog update"
                    commit id: "Sem Ver RC" tag: "v1.4.0-rc" type: HIGHLIGHT
                    commit id: "Revert HEAD" type: REVERSE

                    checkout "main / master"
                    merge release id: "[NEW] v1.4.0" type: HIGHLIGHT tag: "v1.4.0"
            ```

4. **Code Review PR on Github**

    Go to PRs to 'master':  
    https://github.com/boromir674/cookiecutter-python-package/pulls?q=is%3Apr+is%3Aopen+base%3Amaster

5. **Revert RC Sem Ver commit**
    ```shell
    export GIT_BR='release'
    git fetch
    # if local release does not exist, track remote with a new local release
    git branch --track release "origin/${GIT_BR}" || echo "Local '${GIT_BR}' branch already exists."
    # if local release exists, ensure it tracks remote counterpart
    git branch --set-upstream-to="origin/${GIT_BR}" "${GIT_BR}"
    if [ $? -ne 0 ]; then        
        echo "[ERROR] Remote ${GIT_BR} does not exists"
        echo "The assumption is that there is a PR 'release' --> 'master', requires a 'release' branch"
        echo "[FATAL] Exiting .."
    else   
        git checkout release
        git pull
        git revert HEAD
        git push
    fi
    ```

6. **Merge PR 'release' --> 'master'**
  Sample Commit
  - Subject
    ``[NEW] Py Pkg Gen v2.0.0``

  - Body

**--> !! DONE !! <--**

Now, a new Release should be issued:

```shell
git checkout master && git pull && git push

function parse-version { grep -E -o '^version\s*=\s*\".*\"' pyproject.toml | cut -d'"' -f2; }

export tt="v$(parse-version)"

git tag -d "$tt"; git push origin -d "$tt"
git tag "$tt" && git push origin "$tt" && gh release create "$tt"
```

- `master` branch
- `pypi`
- `dockerhub`
- `readthedocs`

Clean Git with:

```shell
git checkout release && git rebase master && git push && git push origin --delete release-train
for bra in test-distro test-docs test-distro-docs boarding-auto; do git push origin -d "$bra"; done
```
