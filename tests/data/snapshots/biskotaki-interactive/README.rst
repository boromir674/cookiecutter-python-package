BISKOTAKI

Project generated from the https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python cookiecutter

.. start-badges

| |build| |docs| |coverage| |maintainability| |tech-debt|
| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|

|
| **Code:** https://github.com/boromir674/biskotaki
| **Docs:** https://biskotaki.readthedocs.io/en/master/
| **PyPI:** https://pypi.org/project/biskotaki/
| **CI:** https://github.com/boromir674/biskotaki/actions/


Features
========

1. **biskotaki** `python package`

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

Using `pip` is the approved way for installing `biskotaki`.

.. code-block:: sh

    python3 -m pip install biskotaki


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

.. _Github Actions: https://github.com/boromir674/biskotaki/actions

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/biskotaki/blob/master/LICENSE


.. BADGE ALIASES

.. Build Status
.. Github Actions: Test Workflow Status for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/biskotaki/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/biskotaki/actions/workflows/test.yaml?query=branch%3Amaster


.. Documentation

.. |docs| image:: https://img.shields.io/readthedocs/biskotaki/master?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://biskotaki.readthedocs.io/en/master/

.. Code Coverage

.. |coverage| image:: https://img.shields.io/codecov/c/github/boromir674/biskotaki/master?logo=codecov
    :alt: Codecov
    :target: https://app.codecov.io/gh/boromir674/biskotaki

.. PyPI

.. |release_version| image:: https://img.shields.io/pypi/v/biskotaki
    :alt: Production Version
    :target: https://pypi.org/project/biskotaki/

.. |wheel| image:: https://img.shields.io/pypi/wheel/biskotaki?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/biskotaki

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/biskotaki?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/biskotaki

.. Github Releases & Tags

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/biskotaki/v0.0.1/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/biskotaki/compare/v0.0.1..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/biskotaki/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)

.. LICENSE (eg AGPL, MIT)
.. Github License

.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/biskotaki
    :alt: GitHub
    :target: https://github.com/boromir674/biskotaki/blob/master/LICENSE


.. CODE QUALITY

.. Code Climate CI
.. Code maintainability & Technical Debt

.. |maintainability| image:: https://img.shields.io/codeclimate/maintainability/boromir674/biskotaki
    :alt: Code Climate Maintainability
    :target: https://codeclimate.com/github/boromir674/biskotaki

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/biskotaki
    :alt: Technical Debt
    :target: https://codeclimate.com/github/boromir674/biskotaki
