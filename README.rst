Python Package Generator
========================

| Python Package Generator supporting 3 different Project `types` to scaffold.
| Emphasizing on CI/CD, Testing and Automation, implemented on top of Cookiecutter.

.. start-badges

| |build| |docs| |coverage| |ossf| |maintainability| |codacy| |tech-debt| |black|
| |release_version| |wheel| |supported_versions| |gh-lic| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|

|
| **Source:** https://github.com/boromir674/cookiecutter-python-package
| **Docs:** https://python-package-generator.readthedocs.io/en/master/
| **PyPI:** https://pypi.org/project/cookiecutter-python/
| **CI:** https://github.com/boromir674/cookiecutter-python-package/actions/


Features
========

1. Scaffold a modern `ready-to-develop` Python Package (see `Quickstart`_)
2. Automatically generate over 24 files, to setup `Test Suite`, `build` scripts & CI Pipeline
3. **Python Package Template** (source code at `src/cookiecutter_python/`_) implemented as a `Cookiecutter`
4. Extensively **Tested** on various systems, factoring the below:
   
   a. System's platform: **"Linux"**, **"MacOS"** & **"Windows"**
   b. System's Python: **3.7**, **3.8**, **3.9** & **3.10**, **3.11**

    See the `Test Workflow` on the `CI`_ server.

Auto Generated Sample Package **Biskotaki**
-------------------------------------------

Check the **Biskotaki** *Python Package Project*, for a taste of the project structure and capabilities this Template can generate!

It it entirely generated using this **Python Package Template:**


| **Source Code** hosted on *Github* at https://github.com/boromir674/biskotaki
| **Python Package** hosted on *pypi.org* at https://pypi.org/project/biskotaki/
| **CI Pipeline** hosted on *Github Actions* at https://github.com/boromir674/biskotaki/actions


Generated Python Package Features
---------------------------------

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


Quickstart
==========

Installation
------------

    .. code-block:: shell

        pip install --user cookiecutter-python


Usage
-----

Open a console/terminal and run:

  .. code-block:: sh

      generate-python

Now, you should have generated a new Project for a Python Package, based on the `Template`_!

    Just 'enter' (`cd` into) the newly created directory, ie `cd <my-great-python-package>`.

| Develop your package's **Source Code** (`business logic`) inside `src/my_great_python_package` dir :)
| Develop your package's **Test Suite** (ie `unit-tests`, `integration tests`) inside `tests` dir :-)


Try Running the Test Suite!

    .. code-block:: shell

        tox


Read the Documentation's `Use Cases`_ section for more on how to leverage your generated Python Package features.


License
=======

|gh-lic|

* `GNU Affero General Public License v3.0`_


Free/Libre and Open Source Software (FLOSS)
-------------------------------------------

|ossf|




.. URL LINKS

.. _Cookiecutter documentation: https://cookiecutter.readthedocs.io/en/stable/

.. _CI: https://github.com/boromir674/cookiecutter-python-package/actions

.. _tox: https://tox.wiki/en/latest/

.. _pytest: https://docs.pytest.org/en/7.1.x/

.. _build: https://github.com/pypa/build

.. _pypi.org: https://pypi.org/

.. _test.pypi.org: https://test.pypi.org/

.. _mypy: https://mypy.readthedocs.io/en/stable/

.. _Github Actions: https://github.com/boromir674/cookiecutter-python-package/actions

.. _src/cookiecutter_python/: https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

.. _Template: https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

.. _Use Cases: https://python-package-generator.readthedocs.io/en/master/contents/30_usage/index.html#new-python-package-use-cases

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE

.. _isort: https://pycqa.github.io/isort/

.. _black: https://black.readthedocs.io/en/stable/



.. BADGE ALIASES

.. Build Status
.. Github Actions: Test Workflow Status for specific branch <branch>

.. |build| image:: https://img.shields.io/github/actions/workflow/status/boromir674/cookiecutter-python-package/test.yaml?link=https%3A%2F%2Fgithub.com%2Fboromir674%2Fcookiecutter-python-package%2Factions%2Fworkflows%2Ftest.yaml%3Fquery%3Dbranch%253Amaster
   :alt: GitHub Workflow Status (with event)

.. build target https://github.com/boromir674/cookiecutter-python-package/actions/workflows/test.yaml?query=branch%3Amaster


.. Documentation

.. |docs| image:: https://img.shields.io/readthedocs/python-package-generator/master?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://python-package-generator.readthedocs.io/en/master/

.. Code Coverage

.. |coverage| image:: https://img.shields.io/codecov/c/github/boromir674/cookiecutter-python-package/master?logo=codecov
    :alt: Codecov
    :target: https://app.codecov.io/gh/boromir674/cookiecutter-python-package

.. PyPI

.. |release_version| image:: https://img.shields.io/pypi/v/cookiecutter_python
    :alt: Production Version
    :target: https://pypi.org/project/cookiecutter-python/

.. |wheel| image:: https://img.shields.io/pypi/wheel/cookiecutter-python?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/cookiecutter-python

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/cookiecutter-python?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/cookiecutter-python


.. Github Releases & Tags

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v1.8.2/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v1.8.2..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)


.. LICENSE (eg AGPL, MIT)
.. Github License

.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/cookiecutter-python-package
    :alt: GitHub
    :target: https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE


.. Free/Libre Open Source Software
.. Open Source Software Best Practices

.. |ossf| image:: https://bestpractices.coreinfrastructure.org/projects/5988/badge
    :alt: OpenSSF
    :target: https://bestpractices.coreinfrastructure.org/en/projects/5988


.. CODE QUALITY

.. Codacy
.. Code Quality, Style, Security

.. |codacy| image:: https://app.codacy.com/project/badge/Grade/5be4a55ff1d34b98b491dc05e030f2d7
    :alt: Codacy
    :target: https://app.codacy.com/gh/boromir674/cookiecutter-python-package/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=boromir674/cookiecutter-python-package&amp;utm_campaign=Badge_Grade


.. Code Climate CI
.. Code maintainability & Technical Debt

.. |maintainability| image:: https://api.codeclimate.com/v1/badges/1d347d7dfaa134fd944e/maintainability
   :alt: Maintainability
   :target: https://codeclimate.com/github/boromir674/cookiecutter-python-package/

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/cookiecutter-python-package
    :alt: Code Climate technical debt
    :target: https://codeclimate.com/github/boromir674/cookiecutter-python-package/


.. Code Style with Black

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Black
    :target: https://github.com/psf/black
