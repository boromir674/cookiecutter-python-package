========================
Python Package Generator
========================

| |build| |coverage| |docs| |maintainability| |codacy| |tech-debt|
| |release_version| |wheel| |supported_versions| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|
| |pypi_stats| |ossf| |ruff| |black| |gh-lic|

|
| **Generate** Python Project and enjoy **streamlined DevOps** using a powerful **CI/CD Pipeline.**
|
| **Documentation** available at https://python-package-generator.readthedocs.io/.


What's included?
================

* **Generator** of **Python Project** (see `Quickstart`_), with **CLI** for **Linux**, **MacOS**, and **Windows**
* **Option** to Generate Python Package designed as `module`, `module+cli`, or `pytest-plugin`!
* Scaffold over **24 files**, from `Template`_, to have a `ready-to-develop` **Project equipped** with:

  * Fully-featured **CI/CD Pipeline**, running on `Github Actions`_, defined in `.github/`
  * **Continuous Delivery** to *PyPI* (i.e. `pypi.org`_, `test.pypi.org`_) and *Dockerhub*
  * **Continuous Integration**, with **Test Suite** running `pytest`_, located in the `tests` dir
  * **Continuous Documentation**, building with `mkdocs` or `sphinx`, and hosting on `readthedocs`, located in the `docs` dir
  * **Static Type Checking**, using `mypy`_
  * **Lint** *Check* and `Apply` commands, using the fast `Ruff`_ linter, along with standard `isort`_, and `black`_
  * **Build Command**, using the `build`_ python package



What to expect?
===============

You can to be up and running with a new Python Package, and run workflows on Github Actions, such as:

.. image is expected to mostly be rendered on github.com, pypi.org, readthedocs.io
   in any case we care for these pages. Adjust images props (ie width if needed)

.. image:: https://raw.githubusercontent.com/boromir674/cookiecutter-python-package/master/docs/assets/CICD-Pipe.png
   :alt: CI Pipeline, running on Github Actions, for a Biskotaki Python Package
   :align: center
   :width: 100%

Link: https://github.com/boromir674/biskotaki/actions/runs/4157571651

1. **CI Pipeline**, running on `Github Actions`_, defined in `.github/`

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`
      2. Python Interpreters: `3.7`, `3.8`, `3.9`, `3.10`, `3.11`, `3.12`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`
   c. **Artifact** store of **Source** and **Wheel** Distributions, factoring Platform and Python Version


Auto Generated Sample Package **Biskotaki**
-------------------------------------------

Check the **Biskotaki** *Python Package Project*, for a taste of the project structure and capabilities this Template can generate!

It it entirely generated using this **Python Package Template:**

| **Source Code** hosted on *Github* at https://github.com/boromir674/biskotaki
| **Python Package** hosted on *pypi.org* at https://pypi.org/project/biskotaki/
| **CI Pipeline** hosted on *Github Actions* at https://github.com/boromir674/biskotaki/actions


Quickstart
==========

To **install** the latest ``Generator`` in your environment, run:

.. code-block:: shell

    pip install cookiecutter-python

The ``generate-python`` (executable) CLI should now be available in your environment.

Next, **create** a file, let's call it ``gen-config.yml``, with the following content:

.. code-block:: yaml

    default_context:
        project_name: Demo Generated Project
        project_type: module+cli
        full_name: John Doe
        email: john.doe@something.org
        github_username: john-doe
        project_short_description: 'Demo Generated Project Description'
        initialize_git_repo: 'no'
        interpreters: {"supported-interpreters": ["3.8", "3.9", "3.10", "3.11"]}


To **generate** a Python Package Project, run:

.. code-block:: sh

    mkdir gen-demo-dir
    cd gen-demo-dir
    
    generate-python --config-file ../gen-config.yml --no-input


Now, you should have generated a new Project for a Python Package, based on the `Template`_!

The Project should be located in the newly created ``demo-generated-project`` directory.


To leverage all out-of-the-box development operations (ie scripts), install `tox`_:

.. code-block:: shell

    python3 -m pip install --user 'tox==3.27.1'

To verify tox available in your environment, run: ``tox --version``


Please, do a `cd` into the newly created directory, ie `cd <my-great-python-package>`.

To run the Test Suite, `cd` into the newly created Project folder, and run:

.. code-block:: shell

    tox -e dev

All Tests should pass, and you should see a `coverage` report!


To run Type Checking against the Source Code, run:

.. code-block:: shell

    tox -e type

All Type Checks should pass!


To setup a Git Repository, run:

.. code-block:: shell

    git init
    git add .
    git checkout -b main
    git commit -m "Initial commit"


To setup a Remote Repository, run for example:

.. code-block:: shell

    git remote add origin <remote-repository-url>
    git push -u origin main


To trigger the CI/CD Pipeline, run:

.. code-block:: shell

    git push

Navigate to your github.com/username/your-repo/actions page, to see the CI Pipeline running!

| Develop your package's **Source Code** (`business logic`) inside `src/my_great_python_package` dir :)
| Develop your package's **Test Suite** (ie `unit-tests`, `integration tests`) inside `tests` dir :-)

Read the Documentation's `Use Cases`_ section for more on how to leverage your generated Python Package features.


Next Steps
----------

To prepare for an Open Source Project Development Lifecycle, you should visit the following websites:

* PyPI, test.pypi.org, Dockerhub, and Read the Docs, for setting up Release and Documentation Pipelines
* github.com/your-account to configure Actions, through the web UI
* Codecov, Codacy, and Codeclimate, for setting up Automated Code Quality, with CI Pipelines
* https://www.bestpractices.dev/ for registering your Project for OpenSSF Best Practices Badge

**Happy Developing!**

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

.. _Template: https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python/%7B%7B%20cookiecutter.project_slug%20%7D%7D

.. _Use Cases: https://python-package-generator.readthedocs.io/en/master/contents/30_usage/index.html#new-python-package-use-cases

.. _GNU Affero General Public License v3.0: https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE

.. _Ruff: https://docs.astral.sh/ruff/

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

.. |pypi_stats| image:: https://img.shields.io/pypi/dm/cookiecutter-python?logo=pypi&logoColor=%23849ED9&color=%23849ED9&link=https%3A%2F%2Fpypi.org%2Fproject%2Fcookiecutter-python%2F&link=https%3A%2F%2Fpypistats.org%2Fpackages%2Fcookiecutter-python
    :alt: PyPI - Downloads
    :target: https://pypistats.org/packages/cookiecutter-python

.. Github Releases & Tags

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v2.5.5/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v2.5.5..master

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
   :target: https://codeclimate.com/github/boromir674/cookiecutter-python-package/maintainability

.. |tech-debt| image:: https://img.shields.io/codeclimate/tech-debt/boromir674/cookiecutter-python-package
    :alt: Code Climate technical debt
    :target: https://codeclimate.com/github/boromir674/cookiecutter-python-package/

.. Ruff linter for Fast Python Linting

.. |ruff| image:: https://img.shields.io/badge/code%20style-ruff-000000.svg
    :alt: Ruff
    :target: https://docs.astral.sh/ruff/

.. Code Style with Black

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Black
    :target: https://github.com/psf/black
