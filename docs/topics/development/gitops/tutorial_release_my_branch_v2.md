[//]: # (This Turorial is part of the Gitops Release - V2 Process)

# **Tutorial:** initiate the `Publish my Branch` Flow

Assuming Github and Dev Environment, are properly setup.

1. **Run in shell console**

    ```shell
    git-tag auto-release
    ```

    This **pushes** the `auto-release` **tag**, which "acts" as a `git event`.

    This, in turn, **triggers** the [**`load-to-rt.yml`**](https://github.com/boromir674/cookiecutter-python-package/.github/workflows/load-to-rt.yml) workflow:

      1. `Merges` 'User Branch' to 'boarding-auto'

        ```mermaid
        %%{init: { 'logLevel': 'debug', 'gitGraph': {'showBranches': true,
            'rotateCommitLabel': false, 'showCommitLabel':true,
            'mainBranchName': 'main / master'}} }%%

            gitGraph
                commit id: "1.2.0" type: HIGHLIGHT tag: "v1.2.0"
                commit id: "1.2.1" type: HIGHLIGHT tag: "v1.2.1"
                commit id: "1.3.0" type: HIGHLIGHT tag: "v1.3.0"
                branch boarding-auto
                branch "User Br"
                commit
                commit id: "new feat"
                checkout boarding-auto
                merge "User Br" type: HIGHLIGHT id: "Cross-Platform TESTS"
        ```

      2. Automated **`Cross-Platform Tests`,** happen on the CI (on `boarding-auto` branch).

      3. **`PR`** 'boarding-auto' --> 'release-train', and **`merge`** if **PR OK**
        **PR OK** if **`Cross-Platform Tests`** PASSED (see previous)

        ```mermaid
        %%{init: { 'logLevel': 'debug', 'gitGraph': {'showBranches': true,
            'rotateCommitLabel': false,
            'showCommitLabel':true,'mainBranchName': 'main / master'}} }%%
            gitGraph
                commit id: "1.2.0" type: HIGHLIGHT tag: "v1.2.0"
                commit id: "1.2.1" type: HIGHLIGHT tag: "v1.2.1"
                commit id: "1.3.0" type: HIGHLIGHT tag: "v1.3.0"
                branch release-train
                branch boarding-auto
                commit id: "MERGED User Br"
                checkout release-train
                merge boarding-auto id: "CI TESTS" type: HIGHLIGHT
        ```

      4. Automated **`CI Tests`,** happen on the CI (on `release-train` branch).
      5. **`PR`** 'release-train' --> 'release', and **`merge`** if *PR OK*
        **PR OK** if **`CI Tests`** PASSED (see previous)

        ```mermaid
        %%{init: { 'logLevel': 'debug', 'gitGraph': {'showBranches': true, 'rotateCommitLabel': false,
            'showCommitLabel':true,'mainBranchName': 'main / master'}} }%%
            gitGraph
                commit id: "1.2.0" type: HIGHLIGHT tag: "v1.2.0"
                commit id: "1.2.1" type: HIGHLIGHT tag: "v1.2.1"
                commit id: "1.3.0" type: HIGHLIGHT tag: "v1.3.0"
                branch release
                branch release-train
                commit id: "MERGED Boarding Auto"
                checkout release
                merge release-train id: "CI TESTS" type: HIGHLIGHT
        ```

      6. Automated **`CI Tests`,** happen on the CI (on `release` branch).

    If **all above succeeded**, then the `release` branch is in a **good state** to proceed with **publishing**.
    
2. Now, sync your `release` local branch, by **running:**
    ```shell
    git fetch && (git checkout release || git branch --track release origin/release) && git pull origin release`
    ```

3. **Run interactive script**

    ```shell
    ./scripts/auto-release.sh
    ```

    This should:

      1. `Ask` for new *Release Sem Ver*
      2. `Ask` user to *Update Changelog themselves*
      3. **`Publish`** a **`Release Candidate`** `Distro`, aka **`Test Deployment`**

        ```mermaid
        %%{init: { 'logLevel': 'debug', 'gitGraph': {'showBranches': true, 'showCommitLabel':true,
            'mainBranchName': 'main / master'}} }%%
            gitGraph
                commit id: "1.2.0" type: HIGHLIGHT tag: "v1.2.0"
                commit id: "1.2.1" type: HIGHLIGHT tag: "v1.2.1"
                commit id: "1.3.0" type: HIGHLIGHT tag: "v1.3.0"
                branch release
                commit id: "MERGED Release Train"
                commit id: "Sem Ver bump"
                commit id: "update Changelog"
                commit id: "RC Sem Ver" tag: "v1.4.0-rc" type: HIGHLIGHT

        ```

        Pushing a `tag` with **-rc** suffix, such as `v1.4.0-rc`, **triggers** the **CI/CD Pipeline** for a **`Release Candidate`** Publication (ie upload to test.pypi.org).

        Such process involves:

        - **Stress Testing** the Distro, by making Builds on different Platforms,
         running different Python Interpreters: {`linux`, `macos`, `windows`} **x** {`3.10`, `3.11`, `3.12`}
        - **Publishing / Deploying** to `Test Environment` **test.pypi.org**

      4. **`PR`** 'release' --> 'master', and **`merge`** if **PR OK**
        **PR OK** if:

        - **`Test Deployment`** PASSED, see previous step *iii*
        - **CI is Green** on Branch's Head (latest / most-recent commit)
        - **Code Review** - APPROVED

4. **Approve PR on `master`**, on Github

    [https://github.com/boromir674/cookiecutter-python-package/pulls?q=is%3Apr+is%3Aopen+base%3Amaster](https://github.com/boromir674/cookiecutter-python-package/pulls?q=is%3Apr+is%3Aopen+base%3Amaster)

5. And **NOW**, if **PR OK**, **`Auto Merge`** 'release' --> 'master'

    ```mermaid
    %%{init: { 'logLevel': 'debug', 'gitGraph': {'showBranches': true, 'showCommitLabel':true,'mainBranchName': 'main / master'}} }%%
        gitGraph
            commit id: "Gen 1.2.0" type: HIGHLIGHT tag: "v1.2.0"
            commit id: "Gen 1.2.1" type: HIGHLIGHT tag: "v1.2.1"
            commit id: "Gen 1.3.0" type: HIGHLIGHT tag: "v1.3.0"
            branch release
            commit id: "MERGED Release Train"
            commit id: "Sem Ver bump"
            commit id: "update Changelog"
            commit id: "RC Sem Ver" tag: "v1.4.0-rc" type: HIGHLIGHT

            checkout "main / master"
            merge release id: "Gen 1.4.0" type: HIGHLIGHT tag: "v1.4.0"
    ```

**--> !! DONE !! <--**

Now, a new Release should be issued:

- `master` branch
- `pypi`
- `dockerhub`
- `readthedocs`

If Automation omitted any of the above, run below:

```shell
git checkout master && git pull && git push
prod_tag="v$(./scripts/parse-version.sh)"
git-tag "$prod_tag" && gh release create "$prod_tag"
```


## MISC

```sh
export tt=v1.12.1
gh release create "$tt" dist/* --verify-tag --generate-notes --notes "Release Notes: {% raw %}${{ github.event.head_commit.message }}{% endraw %}"
```

To be consistent with already published GH Releases at time of writing (2024/01):
* omit --title flag so in github UI, content start directly below the
  git tag, which is rendered as the top section rendered as clickable link
* omit --notes-start-tag string param

* use --generate-notes to generate the automatic content
* here we Prepend some content passed as --notes string param above the
  auto-generated notes content
  run: |
    gh release create "{% raw %}${{ github.ref }}{% endraw %}" dist-local/* --verify-tag \
      --generate-notes \
      --notes "Release Notes: {% raw %}${{ github.event.head_commit.message }}{% endraw %}"

!!! Note
    
    Fails if tag not pushed on remote

!!! Tip
    
    use  -p, --prerelease  to publish it as pre-release
    use  -F, --notes-file file   to possibly Prepend content from file
