Cookiecutter Python Package
===========================

Python Package (pypi) Cookiecutter, with emphasis on CI/CD and automation.

.. start-badges

| |build| |release_version| |wheel| |supported_versions| |commits_since_specific_tag_on_master| |commits_since_latest_release|


|
| **Source Code:** https://github.com/boromir674/cookiecutter-python-package
| **Pypi Package:** https://pypi.org/project/cookiecutter-python/
|


.. Test Workflow Status on Github Actions for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/cookiecutter-python-package/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/actions/workflows/test.yaml?query=branch%3Amaster

.. above url to workflow runs, filtered by the specified branch

.. |release_version| image:: https://img.shields.io/pypi/v/cookiecutter_python
    :alt: Production Version
    :target: https://pypi.org/project/cookiecutter_python/

.. |wheel| image:: https://img.shields.io/pypi/wheel/cookiecutter-python?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/cookiecutter_python

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/cookiecutter-python?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/cookiecutter_python

.. |supported_versions_old| image:: https://img.shields.io/pypi/pyversions/cookiecutter_python.svg
    :alt: Supported Python versions
    :target: https://pypi.org/project/cookiecutter_python

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v0.5.0/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v0.5.0..master

.. |commits_since_latest_release| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v0.5.0..master


.. |commits_since| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v0.5.0/master?logo=github
    :alt: GitHub commits on branch, since tagged version
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v0.5.0..master



.. |circleci| image:: https://circleci.com/gh/boromir674/cookiecutter-python-package/tree/master.svg?style=shield
    :alt: CircleCI
    :target: https://circleci.com/gh/boromir674/cookiecutter-python-package/tree/master

.. |codecov| image:: https://img.shields.io/codecov/c/github/boromir674/cookiecutter-python-package/master?logo=codecov
    :alt: Codecov
    :target: https://codecov.io/gh/boromir674/cookiecutter-python-package


.. |better_code_hub| image:: https://bettercodehub.com/edge/badge/boromir674/cookiecutter-python-package?branch=master
    :alt: Better Code Hub
    :target: https://bettercodehub.com/


.. |sc1| image:: https://img.shields.io/scrutinizer/quality/g/boromir674/cookiecutter-python-package/master?logo=scrutinizer&style=flat
    :alt: Scrutinizer code quality
    :target: https://scrutinizer-ci.com/g/boromir674/cookiecutter-python-package/?branch=master




Features
========

- Python Package Project generation
- CI pipeline to test against multiple Python versions and Platforms
- One-line commands for DevOps activities such as 'package', 'build', 'deploy'
- Test Suite, using Pytest


Prerequisites
=============

You need to have Cookiecutter installed.
Check the `Cookiecutter documentation`_ pages for more on Cookiecutter.


Usage
=====
Open a console/terminal and run:

.. code-block:: sh

    cookiecutter gh:boromir674/cookiecutter-python-package


This will generate a new `Python Package Project` (in the currect dir), using the template from github.
It shall prompt you to enter the necessary initial information to generate the project in a typical cookiecutter fashion.


Modifying the Template
======================

You can always adjust the template to your needs, before generating a new Project.

Open a console/terminal and run:

.. code-block:: bash

    git clone git@github.com:boromir674/cookiecutter-python-package.git
    cd cookiecutter-python-package


Now, you should be inside the `cookiecutter-python-package` repository (directory)
and the actual Template, that you can modify, is inside the `src/cookiecutter_python` sub directory.

After, finishing the modifications you can run something like:

.. code-block:: bash

    cookiecutter src/cookiecutter_python --output-dir <your-new-project-dir>


License
=======

* Free software: Affero GNU General Public License v3.0



.. URL LINKS

.. _Cookiecutter documentation: https://cookiecutter.readthedocs.io/en/stable/
