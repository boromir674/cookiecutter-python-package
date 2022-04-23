{{ cookiecutter.project_name|upper }}

{{ cookiecutter.project_short_description }}

.. start-badges

| |build| |release_version| |wheel| |supported_versions| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|


|
| **Source Code:** https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
| **Pypi Package:** https://pypi.org/project/{{ cookiecutter.pkg_name }}/
|


.. Test Workflow Status on Github Actions for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/actions/workflows/test.yaml?query=branch%3Amaster

.. above url to workflow runs, filtered by the specified branch

.. |release_version| image:: https://img.shields.io/pypi/v/{{ cookiecutter.pkg_name }}
    :alt: Production Version
    :target: https://pypi.org/project/{{ cookiecutter.pkg_name }}/

.. |wheel| image:: https://img.shields.io/pypi/wheel/{{ cookiecutter.pkg_name|replace('_', '-') }}?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/{{ cookiecutter.pkg_name }}

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.pkg_name|replace('_', '-') }}?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/{{ cookiecutter.pkg_name }}

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/v{{ cookiecutter.version }}/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/compare/v{{ cookiecutter.version }}..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)


Features
========

- TODO-feature 1
- TODO-feature 2

Prerequisites
=============

You need to have Python installed.

Installation
============

Using `pip` is the approved way for installing `{{ cookiecutter.pkg_name }}`.

.. code-block:: sh

    python3 -m pip install {{ cookiecutter.pkg_name }}


Usage
=====

TODO

License
=======

* Free software: Affero GNU General Public License v3.0
