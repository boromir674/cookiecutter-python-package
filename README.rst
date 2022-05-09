Cookiecutter Python Package
===========================

Python Package (pypi) Cookiecutter, with emphasis on CI/CD and automation.

.. start-badges

| |build| |docs| |release_version| |wheel| |supported_versions| |commits_since_specific_tag_on_master| |commits_since_latest_github_release| |ossf|

|
| **Source:** https://github.com/boromir674/cookiecutter-python-package
| **Docs:** https://python-package-generator.readthedocs.io/en/master/
| **PyPI:** https://pypi.org/project/cookiecutter-python/
| **CI:** https://github.com/boromir674/cookiecutter-python-package/actions/


Features
========

1. Fresh **Python Package Project Generation**, "packaged" with a **Test Suite** and a **CI** Pipeline (see `Quickstart`_)
2. **Python Package Template** (source code at `src/cookiecutter_python/`_) implemented as a `Cookiecutter`
3. **Tested** on python versions **3.6, 2.7, 3.8, 3.9 and 3.10**, for both **"Linux"** and **"MacOS"** platforms (see `Test Workflow` on `CI`_)

You can check the **Biskotaki** *Python Package Project*, which was entirely generated using this **Python Package Template:**


| **Source Code** hosted on *Github* at https://github.com/boromir674/biskotaki
| **Python Package** hosted on *pypi.org* at https://pypi.org/project/biskotaki/
| **CI Pipeline** hosted on *Github Actions* at https://github.com/boromir674/biskotaki/actions


Generated Python Package Features
---------------------------------

1. **Test Suite** using `pytest`_
2. **Parallel Execution** of Unit Tests, on multiple cpu's
3. **Automation**, using `tox`_

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build`_ python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers
   d. **Type Check Command**, using `mypy`_
   e. **Lint** *Check* and `Apply` commands, using `isort`_ and `black`_
4. **CI Pipeline**, running on `Github Actions`_

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`
      2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`


Quickstart
==========

Prerequisites
-------------

You need to have Cookiecutter installed.
Check the `Cookiecutter documentation`_ pages for more on Cookiecutter.


Usage
-----

Open a console/terminal and run:

  .. code-block:: sh

      git clone git@github.com:boromir674/cookiecutter-python-package.git
      cookiecutter cookiecutter-python-package/src/cookiecutter_python

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


Notes
=====

Currently, since the actual `cookiecutter` template does not reside on the `root` directory
of the repository (but rather in `src/cookiecutter_python`), 'cloning' the repository
locally is required at first.

This was demonstrated in the `Quickstart` section, as well.

For more complex use cases, you can modify the Template and also leverage all of
`cookiecutter`'s features, according to your needs.


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

.. _Use Cases: https://python-package-generator.readthedocs.io/en/master/usage/use_cases.html

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE

.. _isort: https://pycqa.github.io/isort/

.. _black: https://black.readthedocs.io/en/stable/


.. BADGE ALIASES

.. Test Workflow Status on Github Actions for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/cookiecutter-python-package/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/actions/workflows/test.yaml?query=branch%3Amaster

.. above url to workflow runs, filtered by the specified branch

.. |docs| image:: https://img.shields.io/readthedocs/python-package-generator/master?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://python-package-generator.readthedocs.io/en/master/

.. |release_version| image:: https://img.shields.io/pypi/v/cookiecutter_python
    :alt: Production Version
    :target: https://pypi.org/project/cookiecutter-python/

.. |wheel| image:: https://img.shields.io/pypi/wheel/cookiecutter-python?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/cookiecutter-python

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/cookiecutter-python?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/cookiecutter-python

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v0.9.0/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v0.9.0..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)


.. |codecov| image:: https://img.shields.io/codecov/c/github/boromir674/cookiecutter-python-package/master?logo=codecov
    :alt: Codecov
    :target: https://app.codecov.io/gh/boromir674/cookiecutter-python-package

.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/boromir674/cookiecutter-python-package?branch=master
    :alt: Better Code Hub
    :target: https://bettercodehub.com/


.. Github License (eg AGPL, MIT)
.. |gh-lic| image:: https://img.shields.io/github/license/boromir674/cookiecutter-python-package
    :alt: GitHub
    :target: https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE


.. |ossf| image:: https://bestpractices.coreinfrastructure.org/projects/5988/badge
    :alt: OpenSSF
    :target: https://bestpractices.coreinfrastructure.org/en/projects/5988
