=========
Changelog
=========

1.4.1 (2022-06-07)
==================

Changes
^^^^^^^

refactor
""""""""
- decouple dialog creation

chore
"""""
- satisfy prospector linter even better


1.4.0 (2022-06-06)
==================

Add a CLI as an entrypoint to your Python Package
-------------------------------------------------

This release enables the user to optionally provide their Python Package with
a Command Line Interface (CLI) as an entrypoint.
The *add_cli* Generator Variable has been added to behave as an enable/disable
'switch'.

Changes
^^^^^^^

feature
"""""""
- add 'dev' & 'dev-cov' envs, designed to run locally with 'python3' from PATH
- allow user to scaffold a cli with an entrypoint when installing their package

fix
"""
- use a proper name for the test case
- remove hardcoded values and add templated ones

test
""""
- verify that when add_cli = 'no', there are no cli related files generated

development
"""""""""""
- add 'dev' & 'dev-cov' envs, designed to run locally with 'python3' from PATH

refactor
""""""""
- use the 'get_object' fixture from the 'pytest-object-getter' (pypi) package ;-)


1.3.0 (2022-05-31)
==================

Python Interpreters Support and Test
------------------------------------

This release allows the user to select the Python Interpreters they wish their Project
to support and be tested on.
The generator then creates the Test Matrix in the CI config file, which factors in the
Python Interpreter versions supplied by the user. 

Consistent with the currect behaviour of the cli, passing the '--no-input' flag,
instructs the Generator to try find the selected interpreters in a config yaml file,
if given, or else to use the information in the cookiecutter.json.

If the '--no-input' flag is missing, then the user is asked for input, through
their console.
The input is read by supplying an interactive console dialog, which allows the user to
easily select the interpreters they wish to support, by enabling or disabling
'check boxes' through their console.

Development
-----------

All tox environments related to 'Linting' now all do by default a 'check'.
Doing a 'check' means returning a 0 as exit code in case the check is successfull
and it is suitable for local and remote running on a CI server.

The aforementioned environments are 'lint', 'black', 'isort':
- tox -e lint
- tox -e black
- tox -e isort

Optionally, running as below will modify the source code to comply with
each respective 'lint check'.

Running environment 'lint', 'black', 'isort' with 'lint apply' enabled:
- *APPLY_LINT= tox -e lint*
- *APPLY_BLACK= tox -e black*
- *APPLY_ISORT= tox -e isort*

Changes
^^^^^^^

feature
"""""""
- generate the Project's CI Test Workflow with a build matrix based on the user's input python interpreters

test
""""
- verify 'pre gen' script exits with 1 in case module name given is incorrect
- write scenarios with/without 'config file' and with/without given 'interpreters'

development
"""""""""""
- add env for integration testing
- add checks for 'scripts' dir, make 'black', 'isort' cmds only do 'lint-check' by default and add switch to allow doing 'lint-apply'

build
"""""
- add PyInquirer '>= 1.0.3 and < 1.1.0' dependency: required by checkbox dialog


1.2.1 (2022-05-27)
==================

Compeltely migrate away from *setup.cfg*.
Add Issue Templates, as markdown files, to help create well documented Issues on github.

Changes
^^^^^^^

ci
""
- do not run py38-path tox env & improve ci steps names
- push generated package to 'auto-generated' branch on 'origin' remote
- do not initialize a git repository after package generation
- refactor parse script to read from pyproject.toml


1.2.0 (2022-05-24)
==================

Changes
^^^^^^^

feature
"""""""
- migrate to poetry from setuptools as 'build-backend'

fix
"""
- add rule in MANIFEST to match tox.ini similar to *.md, etc non-python files
- replace hardcoded values with templated variables

test
""""
- sanity check to double check that 'tox.ini' gets put in generated dir

documentation
"""""""""""""
- rewrite module docstring

ci
""
- use checkout@v3 instead of @v1
- upload sdist & wheel as artefacts
- separate codecov data exchange into dedicated job


1.1.1 (2022-05-17)
==================

Changes
^^^^^^^

documentation
"""""""""""""
- document installation and cli usage


1.1.0 (2022-05-17)
==================

Wrapping everything in a *command line interface* (cli).
Speed up performance by using *futures* for http requests.

Changes
^^^^^^^

feature
"""""""
- allow user to control parameters of the project generation process
- expose project generator through an interactive cli
- add async capabilities to the pre_gen_project.py for faster network bound operations

documentation
"""""""""""""
- demonstrate how to install and use the cli

ci
""
- update workflow to install and use the 'generate-python' cli


1.0.0 (2022-05-11)
==================

Releasing v1.0.0, the first ever v1.* version!
We are confident that the user-facing "interface" of this package is stable
and commit to (continue to) follow `Semantic Versioning`.

As far as changes are concerned, invoking the `project generator`
now adds several new `status badges` in your README, which automatically update based on
their corresponding CI services!

Changes
^^^^^^^

feature
"""""""
- add new status badges and slightly improve content

fix
"""
- clean files and configs

documentation
"""""""""""""
- explain which generated file governs which component (ie ci code, tests code, etc)


0.11.0 (2022-05-11)
===================

The `Project Generator` now scaffolds a reasonably minimum website for your documentation pages!

The (html) website is built out of .rst files using `sphinx` and is ready to be hosted on
readthedocs.org, with just a few clicks' :)


feature
"""""""
- add templated documentation pages & configure website building and hosting on rtd server

fix
"""
- fix integration, by using a config file

documentation
"""""""""""""
- add word 'env' to know spelling list
- improve visibility of Biskotaki pypi package, which is generated from this Template


0.10.1 (2022-05-11)
-------------------

ci
^^
- add rules for automatic Pull Request labelling, with tags: template, ci, test & docs
- add pull request automatic labeling workflow


0.10.0 (2022-05-11)
===================

Enhance the Template's project generated CI config, by adding extra `checks` in Test Jobs and
automating the `integration` with the `codecov.io` hosting service.

Added `checks`
--------------

- Doing a 'Lint check' on the code
- Doing a 'Compliance check' of the resulting packaged distro against python best practices
- Gathering and sending the Test Suite results to the codecov.io service

Code Coverage
-------------

Include `step` in all Test Jobs to gather and send Code Coverage data resulting from running
the Test Suite.

    `Codecov` is to Code Coverage, as `GA` is to Continuous Integration.

    Upon granting permission, `codecov` will start accepting the accumulated results (such as
    Code Coverage data) from all `Test Jobs` during a `build` and provide a web UI featuring
    interactive visualization of the python code and its `coverage` on user-defined granularity
    level, interactive charts of the `coverage` evolution and more.

ci
--
Apply the same CI additions as the ones added for the Template project (see above)!
Namely:

- extra `checks` in the `Test Jobs`
- `integration` with the `codecov.io` Code Coverage hosting service

documentation
-------------
Add some "juicy" **code badges** in `README`, to demonstrate the `status` reported by
the various `CI services` that this repository integrates with. The badges are updated
automatically, as their respective status reporting (web) service `continuously integrates`
(ie triggers per commit) with the `cookiecutter-python-package` Project.

Changes
^^^^^^^

feature
"""""""
- enable lint, distro packaging QA & test results transimission to codecov.io CI service

fix
"""
- fix generated tox ini that had a hard coded value!

documentation
"""""""""""""
- add the changes introduced in this release
- add Codacy Badge to quickly show the reported Code Quality

ci
""
- enable test workflow for tags matching pattern "v*", pull requests to dev & pushes to ci branch
- add job to generate the Biskotaki Python Package from this Template


0.9.0 (2022-05-09)
==================

Changes
^^^^^^^

feature
"""""""
- update generated .gitignore
- add lint check and lint apply tox envs in the generated project
- document the project structure, test infra and ci as changelog entry

fix
"""
- fix the generated tox ini multifactor environments
- add contributing and license rules for generated package

test
""""
- skip test cases needing internet connection for default Test Suite execution
- add test case for running without initializing git repository
- define a test case where we run tox for a newly generated project
- 73% code coverage

documentation
"""""""""""""
- document the get_object fixture
- add instructions on how to Check Lint Rules and apply Lint fixes to satisfy them

ci
""
- ignore post_gen_project.py script because the templated vars make black complain
- add lint check in Test Workflow
- add lint environment, which can check & fix code following our Code Style/Linting strategy
- add isort environment and run on code
- add configuration for black in pyproject.toml
- add black environment
- fix type checking for python 3.6
- fix type checking for python 3.8
- enable for pushes to the 'ci' branch


0.8.3 (2022-04-29)
==================

Changes
^^^^^^^

docs
""""
- add CONTRIBUTING.md

dev
"""
- add configuration for code static analysis with `pylint`
- add configuration for code static analysis with `prospector`

ci
""
- add type checking all CI Jobs
