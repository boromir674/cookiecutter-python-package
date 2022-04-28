Cookiecutter Python Package
===========================

Python Package (pypi) Cookiecutter, with emphasis on CI/CD and automation.

.. start-badges

| |build| |release_version| |wheel| |supported_versions| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|

|
| **Source Code:** https://github.com/boromir674/cookiecutter-python-package
| **Pypi Package:** https://pypi.org/project/cookiecutter-python/
| **CI Pipeline:** https://github.com/boromir674/cookiecutter-python-package/actions/

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

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v0.7.2/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/cookiecutter-python-package/compare/v0.7.2..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)


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
4. **CI Pipeline**, running on `Github Actions`_

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platfroms: `ubuntu-latest`, `macos-latest`
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

Run Test Suite:

    .. code-block:: shell
        
        tox


Try yourself!
^^^^^^^^^^^^^

You are ready to enjoy some of the package's **features** available out-of-the-box!

For instance:

1. Leverage the supplied `tox environments` to automate various **Testing** and **DevOps** related activities.

   Assuming you have `tox` installed (example installation command: `python3 -m pip install --user tox`)
   and you have done a `cd` into the newly generated Project directory, you can do for example:

   a. Run the **Test Suite** against different combinations of `Python versions` (ie 3.7, 3.8) and different ways of installing (ie 'dev', 'sdist', 'wheel') the `<my_great_python_package>` package:

      .. code-block:: sh

         tox -e "py{3.7, 3.8}-{dev, sdist, wheel}"

   b. Check the code for **compliance** with **best practises** of the `Python packaging ecosystem` (ie PyPI, pip),
      build `sdist` and `wheel` distributions and store them in the `dist` directory:

      .. code-block:: sh

           tox -e check && tox -e build

   c. **Deploy** the package's distributions in a `pypi` (index) server:

      1. Deploy to **staging**, using the `test` pypi (index) server at `test.pypi.org`_:

         .. code-block:: sh

             TWINE_USERNAME=username TWINE_PASSWORD=password PACKAGE_DIST_VERSION=1.0.0 tox -e deploy

      2. Deploy to **production**, using the `production` pypi (index) server at `pypi.org`_:

         .. code-block:: sh

             TWINE_USERNAME=username TWINE_PASSWORD=password PACKAGE_DIST_VERSION=1.0.0 PYPI_SERVER=pypi tox -e deploy

         .. note::
            Setting PYPI_SERVER=pypi indicates to deploy to `pypi.org` (instead of `test.pypi.org`).

      .. note::
         Please modify the TWINE_USERNAME, TWINE_PASSWORD and PACKAGE_DIST_VERSION envronment variables, accordingly.

         TWINE_USERNAME & TWINE_PASSWORD are used to authenticate (user credentials) with the targeted pypi server.

         PACKAGE_DIST_VERSION is used to avoid accidentally uploading distributions of different versions than intented.


2. Leverage the **CI Pipeline** and its **build matrix** to run the **Test Suite** against a combination of
   different Platforms, different Python interpreter versions and different ways of installing the subject Python Package:

    `Trigger` the **Test Workflow** on the **CI server**, by `pushing` a git commit to a remote branch (ie `master` on github).

    `Navigate` to the `CI Pipeline web interface` (hosted on `Github Actions`) and inspect the **build** results!


   .. note::
      You might have already `pushed`, in case you answered `yes`, in the `initialize_git_repo` prompt, while generating the Python Package,
      and in that case, the **Test Workflow** should have already started running!

      Out-of-the-box, `triggering` the **Test Workflow** happens only when pushing to the `master` or `dev` branch.


License
=======

* Free software: Affero GNU General Public License v3.0


Notes
=====

Currently, since the actual `cookiecutter` template does not reside on the `root` directory
of the repository (but rather in `src/cookiecutter_python`), 'cloning' the repository
locally is required at first.

This was demonstrated in the `quickstart` section, as well.

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
