BISKOTAKI GOLD STANDARD

Project generated from https://github.com/boromir674/cookiecutter-python-package/

.. start-badges

| |build| |release_version| |wheel| |supported_versions|
| |docs| |coverage| |maintainability| |tech-debt|
| |ruff| |gh-lic| |commits_since_specific_tag_on_main| |commits_since_latest_github_release|

|
| **Code:** https://github.com/boromir674/biskotaki-gold
| **Docs:** https://biskotaki-gold.readthedocs.io/en/main/
| **PyPI:** https://pypi.org/project/biskotakigold/
| **CI:** https://github.com/boromir674/biskotaki-gold/actions/


Features
========

1. **biskotakigold** `python package`

   a. TODO Document a **Great Feature**
   b. TODO Document another **Nice Feature**
2. Tested against multiple `platforms` and `python` versions


Development
-----------

| Get started:

.. code-block:: shell

    python3 -m pip install --user 'tox<4'

OR: **`pipx install tox`**

Then, to see all out-of-the-box available `tox` commands:

.. code-block:: shell

    tox -a
    

OR **`tox -av`** for showing `description` of each command

Development Notes
~~~~~~~~~~~~~~~~~
Testing, Documentation Building, Scripts, CI/CD, Static Code Analysis for this project.

1. **Test Suite**, using `pytest`_, located in `tests` dir
2. **Parallel Execution** of Unit Tests, on multiple cpu's
3. **Documentation Pages**, hosted on `readthedocs` server, located in `docs` dir
4. **CI/CD Pipeline**, running on `Github Actions`_, defined in `.github/`

   a. **Test Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`, `windows-latest`
      2. Python Interpreters: `3.8`, `3.9`, `3.10`, `3.11`
   b. **Continuous Deployment**
   
      `Production`
      
         1. **Python Distristribution** to `pypi.org`_, on `tags` **v***, pushed to `main` branch
         2. **Docker Image** to `Dockerhub`_, on every push, with automatic `Image Tagging`
      
      `Staging`

         1. **Python Distristribution** to `test.pypi.org`_, on "pre-release" `tags` **v*-rc**, pushed to `release` branch

   c. **Configurable Policies** for `Docker`, and `Static Code Analysis` Workflows
5. **Automation**, using `tox`_, driven by single `tox.ini` file

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build`_ python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers
   d. **Type Check Command**, using `mypy`_
   e. **Lint** *Check* and `Apply` commands, using the fast `Ruff`_ linter, along with `isort`_ and `black`_


Prerequisites
=============

You need to have `Python` installed.

Quickstart
==========

Using `pip` is the approved way for installing `biskotakigold`.

.. code-block:: sh

    python3 -m pip install biskotakigold


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

.. _Dockerhub: https://hub.docker.com/

.. _pypi.org: https://pypi.org/

.. _test.pypi.org: https://test.pypi.org/

.. _mypy: https://mypy.readthedocs.io/en/stable/

.. _Ruff: https://docs.astral.sh/ruff/

.. _isort: https://pycqa.github.io/isort/

.. _black: https://black.readthedocs.io/en/stable/

.. _Github Actions: https://github.com/boromir674/biskotaki-gold/actions

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/biskotaki-gold/blob/main/LICENSE


.. BADGE ALIASES

.. Build Status
.. Github Actions: Test Workflow Status for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/biskotaki-gold/Test%20Python%20Package/main?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/biskotaki-gold/actions/workflows/test.yaml?query=branch%3Amain


.. Documentation

.. |docs| image:: https://img.shields.io/readthedocs/biskotaki-gold/main?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://biskotaki-gold.readthedocs.io/en/main/

.. Code Coverage

.. |coverage| image:: https://img.shields.io/codecov/c/github/boromir674/biskotaki-gold/main?logo=codecov
    :alt: Codecov
    :target: https://app.codecov.io/gh/boromir674/biskotaki-gold

.. PyPI

.. |release_version| image:: https://img.shields.io/pypi/v/biskotakigold
    :alt: Production Version
    :target: https://pypi.org/project/biskotakigold/

.. |wheel| image:: https://img.shields.io/pypi/wheel/biskotakigold?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/biskotakigold

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/biskotakigold?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/biskotakigold

.. Github Releases & Tags

.. |commits_since_specific_tag_on_main| image:: https://img.shields.io/github/commits-since/boromir674/biskotaki-gold/v0.0.1/main?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/biskotaki-gold/compare/v0.0.1..main

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/biskotaki-gold/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)

.. LICENSE (eg AGPL, MIT)
.. Github License

.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/biskotaki-gold
    :alt: GitHub
    :target: https://github.com/boromir674/biskotaki-gold/blob/main/LICENSE


.. CODE QUALITY

.. Ruff linter for Fast Python Linting

.. |ruff| image:: https://img.shields.io/badge/code%20style-ruff-000000.svg
    :alt: Ruff
    :target: https://docs.astral.sh/ruff/

.. Code Climate CI
.. Code maintainability & Technical Debt

.. |maintainability| image:: https://img.shields.io/codeclimate/maintainability/boromir674/biskotaki-gold
    :alt: Code Climate Maintainability
    :target: https://codeclimate.com/github/boromir674/biskotaki-gold

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/biskotaki-gold
    :alt: Technical Debt
    :target: https://codeclimate.com/github/boromir674/biskotaki-gold
