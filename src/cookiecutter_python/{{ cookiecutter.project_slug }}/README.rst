{{ cookiecutter.project_name|upper }}

{{ cookiecutter.project_short_description }}

.. start-badges

| |build| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|


|
| **Source Code:** https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
| **Pypi Package:** https://pypi.org/project/{{ cookiecutter.pkg_name }}/
|


Features
========


1. **{{ cookiecutter.pkg_name }}** `python package`

   a. TODO **Great Feature**
   b. TODO **Nice Feature**

2. **Test Suite** using `Pytest`
3. **Parallel Execution** of Unit Tests, on multiple cpu's
4. **Automation**, using `tox`

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build` python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org` and `test.pypi.org` servers
   d. **Type Check Command**, using `mypy`
   e. **Lint** *Check* and `Apply` commands, using `isort`_ and `black`_
5. **CI Pipeline**, running on `Github Actions`

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`
      2. Python Iterpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`


Prerequisites
=============

You need to have `Python` installed.

Quickstart
==========

Using `pip` is the approved way for installing `{{ cookiecutter.pkg_name }}`.

.. code-block:: sh

    python3 -m pip install {{ cookiecutter.pkg_name }}


TODO demonstrate a use case


License
=======

|gh-lic|

* `GNU Affero General Public License v3.0`_


License
=======

* Free software: GNU Affero General Public License v3.0


.. MACROS/ALIASES

.. start-badges

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

.. Github License (eg AGPL, MIT)
.. |gh-lic| image:: https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
    :alt: GitHub
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/blob/master/LICENSE


.. LINKS

.. _GNU Affero General Public License v3.0: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/blob/master/LICENSE

.. _isort: https://pycqa.github.io/isort/

.. _black: https://black.readthedocs.io/en/stable/
