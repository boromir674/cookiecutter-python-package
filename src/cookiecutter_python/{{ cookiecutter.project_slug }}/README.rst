{{ cookiecutter.project_name|upper }}

{{ cookiecutter.project_short_description }}

.. start-badges

| |build| |docs| |coverage| |maintainability| |better_code_hub| |tech-debt|
| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|

|
| **Code:** https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
| **Docs:** https://{{ cookiecutter.repo_name }}.readthedocs.io/en/master/
| **PyPI:** https://pypi.org/project/{{ cookiecutter.pkg_name|replace('_', '-') }}/
| **CI:** https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/actions/


Features
========

1. **{{ cookiecutter.pkg_name }}** `python package`

   a. TODO Document a **Great Feature**
   b. TODO Document another **Nice Feature**
2. Tested against multiple `platforms` and `python` versions


Development
-----------
Here are some useful notes related to doing development on this project.

1. **Test Suite**, using `pytest`_, located in `tests` dir
2. **Parallel Execution** of Unit Tests, on multiple cpu's
3. **Documentation Pages**, hosted on `readthedocs` server, located in `docs` dir
4. **Automation**, using `tox`_, driven by single `tox.ini` file

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build`_ python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers
   d. **Type Check Command**, using `mypy`_
   e. **Lint** *Check* and `Apply` commands, using `isort`_ and `black`_
5. **CI Pipeline**, running on `Github Actions`_, defined in `.github/`

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`
      2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`


Prerequisites
=============

You need to have `Python` installed.

Quickstart
==========

Using `pip` is the approved way for installing `{{ cookiecutter.pkg_name }}`.

.. code-block:: sh

    python3 -m pip install {{ cookiecutter.pkg_name }}


TODO Document a use case


License
=======

|gh-lic|

* `GNU Affero General Public License v3.0`_


License
=======

* Free software: GNU Affero General Public License v3.0



.. LINKS

.. _tox: https://tox.wiki/en/latest/

.. _pytest: https://docs.pytest.org/en/7.1.x/

.. _build: https://github.com/pypa/build

.. _pypi.org: https://pypi.org/

.. _test.pypi.org: https://test.pypi.org/

.. _mypy: https://mypy.readthedocs.io/en/stable/

.. _isort: https://pycqa.github.io/isort/

.. _black: https://black.readthedocs.io/en/stable/

.. _Github Actions: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/actions

.. _GNU Affero General Public License v3.0: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/blob/master/LICENSE


.. BADGE ALIASES

.. Build Status
.. Github Actions: Test Workflow Status for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/actions/workflows/test.yaml?query=branch%3Amaster


.. Documentation

.. |docs| image:: https://img.shields.io/readthedocs/{{ cookiecutter.repo_name }}/master?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://{{ cookiecutter.repo_name }}.readthedocs.io/en/master/

.. Code Coverage

.. |coverage| image:: https://img.shields.io/codecov/c/github/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/master?logo=codecov
    :alt: Codecov
    :target: https://app.codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}

.. PyPI

.. |release_version| image:: https://img.shields.io/pypi/v/{{ cookiecutter.pkg_name }}
    :alt: Production Version
    :target: https://pypi.org/project/{{ cookiecutter.pkg_name }}/

.. |wheel| image:: https://img.shields.io/pypi/wheel/{{ cookiecutter.pkg_name|replace('_', '-') }}?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/{{ cookiecutter.pkg_name }}

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.pkg_name|replace('_', '-') }}?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/{{ cookiecutter.pkg_name }}

.. Github Releases & Tags

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/v{{ cookiecutter.version }}/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/compare/v{{ cookiecutter.version }}..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)

.. LICENSE (eg AGPL, MIT)
.. Github License

.. |gh-lic| image:: https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
    :alt: GitHub
    :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/blob/master/LICENSE


.. CODE QUALITY

.. Better Code Hub
.. Software Design Patterns

.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}?branch=master
    :alt: Better Code Hub
    :target: https://bettercodehub.com/


.. Code Climate CI
.. Code maintainability & Technical Debt

.. |maintainability| image:: https://img.shields.io/codeclimate/maintainability/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
    :alt: Code Climate Maintainability
    :target: https://codeclimate.com/github/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/maintainability

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
    :alt: Technical Debt
    :target: https://codeclimate.com/github/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/maintainability
