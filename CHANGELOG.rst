=========
Changelog
=========

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
