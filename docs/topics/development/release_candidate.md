# Release Candidate / Test Deployment

From your branch, run:

[//]: # (Start of command block)

```sh
rc_tag=$(grep -E -o '^version\s*=\s*".*"' pyproject.toml | cut -d'"' -f2) rc_tag="${rc_tag}-rc"

git tag "$git_tag" || (git tag -d "$git_tag" && git tag "$git_tag") git push origin -d "$git_tag"; git push origin "$git_tag"

```

[//]: # (End of command block)

This will trigger the CI/CD Pipeline and instruct it to do a **Test Deployment**.

Test Deployment is a full deployment of the package to the test environment.  
It is the closest thing to a real (production) deployment.

The CI/CD Pipeline will:

1. Make wheel builds (and unit test them) for the package using a Job Matrix factoring OS x Python Versions.
2. Perform normal measurements of Code Coverage, Static Code Analysis, and Docker Build.
3. Publish the Python Wheel Distribution in the Test Environment at [test.pypi.org](https://test.pypi.org).
