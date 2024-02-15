
===================================
Release Candidate / Test Deployment
===================================

From your branch, run

.. code-block:: bash

    rc_tag=$(grep -E -o '^version\s*=\s*\".*\"' pyproject.toml | cut -d'"' -f2)
    rc_tag="${rc_tag}-rc"

    git tag "$git_tag" || (git tag -d "$git_tag" && git tag "$git_tag")
    git push origin -d "$git_tag"; git push origin "$git_tag"

This will, trigger the CI/CD Pipeline and instruct it to do a ``Test Deployment``.

| Test Deployment is a full deployment of the package to the test environment.
| And is the closest thing to a real (production) deployment.

.. The CI/CD Pipeline will:
.. 1. make wheel builds (and unit test them) for the package using a Job Matrix factoring OS x Py Versions
.. 2. Do as normal measuring of Code Coverage, Static Code Analysis, Docker Build
.. 3. Publish Python Wheel Distribution in Test Environment, at test.pypi.org

The CI/CD Pipeline will:

1. make wheel builds (and unit test them) for the package using a Job Matrix factoring OS x Py Versions
2. Do as normal measuring of Code Coverage, Static Code Analysis, Docker Build
3. Publish Python Wheel Distribution in Test Environment, at test.pypi.org


