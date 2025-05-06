# Streamline **Documentation** Updates

1. Branch off the `main` branch, and checkout your `topical branch` (`tb`).

2. Create Docs-only changes and commit them to your `tb`.

3. Push the git tag `quick-release` to trigger the Docs Release Workflow on the CI.

   A new PR is expected to **open** from `tb` to a `dedicated docs` branch,  
   and automatically **merge** if the Docs Build passes on the `rtd` CI.

   Then, a new PR is expected to **open** from the `dedicated docs` branch to `main`,  
   with extra commits for the SemVer bump and Changelog updates.

4. Wait for the second PR to open, go to the GitHub web UI to review it, and merge it.

   A new **tag** is expected to be created (on the new main/master commit),  
   and a `PyPI` distribution will be uploaded, a new Docker Image on DockerHub,  
   and a new GitHub Release will be created.

## Workflows References

- **quick-docs.yaml**: Listens to the `quick-release` git tag and merges `tb` → `db` after opening a PR.  
  [Source Code](https://github.com/boromir674/cookiecutter-python-package/blob/master/.github/workflows/quick-docs.yaml)
