=========
Changelog
=========


1.12.3 (2024-02-08)
===================

**Improved Code Coverage.**


Changes
^^^^^^^

test
""""
- verify expected exceptions are thrown, in cases of errors, and add new sanitization test cases

chore
"""""
- chore(gitignore): update .gitignore

ci
""
- trigger Job of merge-rt-in-release only if github.event_name == 'pull_request' && github.event.pull_request.merged == true

release
"""""""
- bump version to 1.12.3


1.12.2 (2024-02-07)
===================

**Regression and Backwards Compatibility - Tests**

This Release features the addition of Automated Regression Test for 'Generator Docs Default Settings'.  
By Default Generator v2.x promises that upon invocation, the generated Project with be configured for
| Doc Builds with Sphinx and RTD Python3.8.  

The Test will fail if Defaults change.  
If Test is fixed, by updating assertion in Test Code, then then this is evidence that if we release these future changes,
they possibly introduce "breaking changes".

Also, we add a new Test on the Dialog Prompts to verify that they prompt the User for each and every one of the Cookiecutter Tempalte Variables.  
If this test fails, then the Dialog System and the Cookiecutter Tempalte Vars are out of Sync, which should be addressed, preventing a Bug from shipping Code with the 2 components being NOT synced.

From this Relase onward, we also start measuring Code Coverage only on Production Code.  
We only measure the 'src' dir, and stop measuring Test Code, in 'tests' dir.

Changes
^^^^^^^

test
""""
- verify Gen Project configured with Sphinx and RTD Py3.8, as advertised Defaults
- verify prompts user for each and everyone of Cookiecutter Template Variables

release
"""""""
- bump version to 1.12.2


1.12.1 (2024-01-29)
===================

Adding Continous Deployment for `Github Release`, with a dedicated **CI Job**.

This Release prepares for new GitOps-based Release Process.
It adopts the concept of `Release Train`, which is represented by a
**dedicated** git branch.

The process is designed to be semi-automatic, since a developer is expected
to:
- input a `Semantic Version`, for bumping the previous **Release** Version
- add a Changelog entry, corresponding to the new **Release**

The process involves `gitops operations`, simple `shell scripts`,
and `github workflows`.


Changes
^^^^^^^

documentation
"""""""""""""
- add Badge to count monthly pypi downloads (#116)

ci
""
- add Job for `gh release create`, and trigger load-to-rt on 'auto-release' tag
- gitops "boarding" on `Release Train`
- gitops "release" User's Branch
- improve messages rendered on github actions web ui

test
""""
- expect either empty log file in PWD, after generator run, or no file at all

refactor
""""""""
- apply new black version 24.1, with the 2024 style

style
"""""
- clean code, by removing obsolete code comments related to cookiecutter callable

release
"""""""
- bump version to 1.12.1


1.12.0 (2024-01-18)
===================

In this release, we fix then [known issue](https://github.com/boromir674/cookiecutter-python-package/issues/63),
when running the `Generator` CLI in `interactive` mode.

**Now**, in case the CLI is ran in `interactive` mode, all interactive dialogs / prompts
are delegated to `Questionnaire`, which is already a python dependency of the `Generator`.

The `Cookiecutter` callable / executable is **now** always called, with the `no_input` boolean
flag set to `True`.

The idea was to refrain from updating our locked `cookiecutter` dependency, from 1.7.x to 2.x,  
for the time being.


Changes
^^^^^^^

feature
"""""""
- support running interactive CLI, without supplying User's Config Yaml file
- populate Context, in pre_main, if interactive mode is ON

test
""""
- make snapshot testinng robust against runtime Calendar Year changes!

refactor
""""""""
- exclude DEBUG-level logs from being emitted in the Console (just in file)
- Ruff, Black, Isort, Mypy

chore
"""""
- remove Handler Chain Infra, since we delegate handling Input to Questionnaire

release
"""""""
- bump version to 1.12.0


1.11.4 (2023-12-25)
===================

| Revisiting the **`Why this Generator?`_** page in the Docs Website.  
| And **updating motivation**, for reader to use our software.

- We update content based on new Developments
- We present it, in 4 top-level arguments: see `Diff`_ on github

.. LINKS

.. _`Why this Generator?`: https://python-package-generator.readthedocs.io/en/master/contents/20_why_this_package.html

.. _Diff: https://github.com/boromir674/cookiecutter-python-package/pull/114/files#diff-1f6c4e1615922e41582cdc651b4dd501a73e90bb6109e18ac5bb526ec2c92297

Changes
^^^^^^^

documentation
"""""""""""""
- redesign Motivation Documentation Page, around 4 Top Level arguments


1.11.3 (2023-12-25)
===================

Changes
^^^^^^^

fix
"""
- fix syntax error in pyproject.toml, causing build process to fail


1.11.2 (2023-12-25)
===================

Changes
^^^^^^^

documentation
"""""""""""""
- improve README
- fix URL link of CI/CD Pipeline, used in Docs site to demonstrate Generated Proj capabilities


1.11.0 (2023-12-24)
===================

Changes
^^^^^^^

feature
"""""""
- drastically improve Developer's Guides section


1.10.0 (2023-12-24)
===================

*Upgrade*, **Docker**, **Code Visualization** and **Docs** *Jobs*, which are
out-of-the-box produced by the `Generator` as part of the **CI/CD Pipeline**
configuration YAML files, to be **Configurable by Policy**.

*Design* a **High-Level** interface, for *configuring the CI/CD Behaviour*, allowing:
- seemless switching between **Policies**, on a per-Job level
- Easy **Override** to `"shutdown" Job"`, ie to *prevent upload*, by-passing `decision-making`
- Easy **Override** to `"force Job"`, ie for *quick trial*, by-passing `decision-making`
 governing desicion-making, on the Workflows/Jobs.

A **Policy** governs how a Job behaves (ie if it should trigger), and each
one yiels a *distinct* behaviour.

At CI runtime, each Job uses its **Policy** and the Status of the Build,
triggered on the CI, to decide if it should `run or not`.

A Job can take into **account** "things" such as:
- whether the current `Build` passed the `Test`'s
- whether the `Test Job` was intentionally skipped
- whether `production code` (ie python distro) changed from previous commit 

Changes
^^^^^^^

feature
"""""""
- support **Policy-based** Workflows/Job, in the **CI/CD Pipeline**
- add **Dev Guides** Page in Docs Website, when selecting `Mkdocs` as Docs Builder

test
""""
- improve automatically derived emulated project to use for Post Hook Unit Tests


1.9.0 (2023-12-22)
==================

Introducing `Ruff` as part of the `Static Code Analysis` Toolchain.  
Generator, now features `CI/CD`, with the `Ruff` Fast Python Linter!

Preparing, to retire `pylint`, in the future, by removing CI Job dedicated to it, at the moment.

Changes
^^^^^^^

feature
"""""""
- introduce `Ruff`, Fast Python Linter, in updated `Developer's Tool chain <https://github.com/boromir674/biskotaki/tree/auto-generated?tab=readme-ov-file#development>`_
- run `Ruff` against code, as part of the Tools included in the `Static Code Analysis` CI Workflow, produced by the **Generator's** Template
- run legacy `Pylint` agaist code, in dedicated Job, for easier potential retirement
- make Template Code pass Ruff Checks/Evaluations
- add `Ruff`, `tox -e ruff`, as available `tox command`` for fast `Static Code Check`

fix
"""
- remove extra but empty Log file, that appears inside the Gen Project

test
""""
- automatically test that Rendered policy_lint.yml CI config is valid YAML
- automatically verify that extra, but empty log file does NOT appear in Gen Proj

documentation
"""""""""""""
- feature Ruff as New Fast Python Linter, and add Ruff Code Badge in README
- mention pytest-explicit as requirement for all test suite features (ie cli flags)

style
"""""
- apply isort and black code "fixes"

refactor
""""""""
- apply Ruff fixes

ci
""
- run Ruff in the Static Code Analysis CI Job and keep running legacy Pylint in separate Job
- remove dedicated docker settings reading Job
- refactor so that some intermediate Jobs are eliminated
- delegate Code Visualization to Reusable Workflow, with configurable execution Policy
- use workflow one-liner instead of bash if-else

chore
"""""
- add 'Snapshot Update' Scripts, and dedicate README for the Process


1.8.7 (2023-12-16)
==================

Changes
^^^^^^^

ci
""
- run 1-Job Test, instead of Stress Tests, on push to master or main branch

release
"""""""
- bump version to 1.8.7


1.8.6 (2023-12-15)
==================

Changes
^^^^^^^

documentation
"""""""""""""
- improve **Quickstart** Gide in README.rst


1.8.3 (2023-12-15)
==================

Changes
^^^^^^^

documentation
"""""""""""""
- mention Documentation Site right after README.rst Subtitle and before badges


1.8.2 (2023-12-15)
==================

Changes
^^^^^^^

ci
""
- remove unused workflow
- fix workflow syntax due to merge confict resolution artifacts


1.8.1 (2023-12-15)
==================

Changes
^^^^^^^

documentation
"""""""""""""
- add shell on-liner for firing up a 'quick-release' event
- add 'Quick Docs Release' Guide & restructure some content based on Diataxis theory

ci
""
- Open PR to master on 'quick-release' event, to release Docs only Updates


1.8.0 (2023-12-12)
==================

Changes
^^^^^^^

feature
"""""""
- New Generator Option allows for `Mkdocs` doc site builder, along with `sphinx` 
- Generator adds python Logging Configuration, with Handlers for streaming to `File` and `Std err`
- Generator adds full CI/CD Pipeline as Github Actions Workflow, introducing new Jobs such as `Docker`, and `PyPI`

fix
"""
- include pytest-run-subprocess in test Extras of Generated Project pyproject.toml

test
""""
- add `Gold Standard` Generated Biskotaki Projects 
- verify `No Regression` of Generator, with exhaustive comparison of Runtime result to `Gold Standard`
- test `Gold Standard` passes `tox -e lint`
- ignore Tests inside Snapshots, during `Test Discovery` of Pytest
- verify `User Config` backwords compatibility, with regard to new `Docs` Generator Feature
- test default gen behaviour related to Docs, is same as before adding mkdocs option
- yaml validation and required/expected workflow vars checks

documentation
"""""""""""""
- fix README badge
- add docstring in backend.post_main:post_main function, to check out-of-the-box CD
- add Docstring, for Cookiecutter Pre Hook, at Module (file/script) level

dev
"""
- add Logging Configuration: DEBUG and above Stream to Std err and Write to Disk

refactor
""""""""
- simplify 'main' code
- simplify 'pre_main' code


1.7.5 (2023-02-05)
==================

| Moving towards fully automated CI/CD pipeline.
| See the .github/workflows/test.yaml file for the workflow (aka pipeline) details.


Changes
^^^^^^^

ci
""
- dedicate separate Job to upload Coverage xml files to Codecov
- dedicate a Job Matrix for running Lint Checks
- publish to pypi Job, configured given a 'test' or 'prod' Github Environment (configured through github web UI)
- draw python dependency graphs, saved as .svg files, for master/dev branches and for tags starting with 'v'

build
"""""
- remove data of apt update after apt install from Dockerfile stage


1.7.4 (2023-01-26)
==================

| Improvements in the CI/CD pipeline running on Github Actions.
| See the .github/workflows/test.yaml file for the workflow (aka pipeline) details.


Changes
^^^^^^^

documentation
"""""""""""""
- check Web Server Result Interface

ci
""
- 'set_github_outputs' Job to pass 'env' vars to GITHUB_OUTPUT
- add flag to turn on/off docker build+publish
- draw deps job based on changes in src dir
- add disable tests flag
- build and push (docker) image to dockerhub
- define (docker) image, where the 'generate-python' cli is installed


1.7.3 (2023-01-15)
==================

Changes
^^^^^^^

fix
"""
- raise a proper subclass of python built-in Exception

documentation
"""""""""""""
- improve documentation

style
"""""
- apply isort in codebase

refactor
""""""""
- satisfy pylint a bit more

build
"""""
- add pinned/locked dependencies defined in poetry.lock
- replace PyInquirer with Questionary package

ci
""
- install dependencies for pydeps Job
- use pydeps == 1.11.0 which supports python3.10 & remove autoprovisioning of tox
- draw dependency graphs in new Job after tests and upload artifacts
- add 'pytest' as a known word to pass spell checking
- remove badges from bettercodehub since the service has shut down
- pin tox to 3.28 in generate workflow
- run pylint in ci and fail job if score is below threshold
- fail pylint step if score is below PYLINT_THRESHOLD variable
- run only unit-tests in ci workflow
- fix ci
- install pinned to 3.28 in ci runner
- debug type checking on windows tox
- skip tox -e lint on windows machine
- remove py36 from ci matrix generation
- fix prospector environment's commands
- `tox -e pydeps`: allow configuration of target dir & allow invoking from outside root dir


1.7.2 (2022-11-13)
==================

Fixing a couple of bugs.

Changes
^^^^^^^

fix
"""
- only generate 'fixtures.py' for pytest-plugin project type
- fix pyproject.toml syntax

documentation
"""""""""""""
- improve documentation


1.7.1 (2022-07-30)
==================

Changes
^^^^^^^

refactor
""""""""
- reduce duplicate code & clean code


1.7.0 (2022-07-11)
==================

Introducing a pre-emptive check of whether a Project registered under the same
name as the one given to the generator, exists on
the readthedocs.org server already.

Changes
^^^^^^^

feature
"""""""
- check if a project with the same slug name, is already registered on the readthedocs server

test
""""
- improve flexibility of testing code

refactor
""""""""
- modularize code and improve dryness of code as well


1.6.1 (2022-07-05)
==================

This is the first Cross-Platform release of the *Python Generator*.
That means, now, we officially support installing and running the
*Python Generator*, apart from Linux and Macos, on Windows machines as well.

Changes
^^^^^^^

test
""""
- manually covert gitpython outputted string paths into Path instances
- use Path from pathlib instead of the os.path module

refactor
""""""""
- remove the 'path_builder' fixture, to reduce test code
- remove depcrecation warning fired by Jinja2 when rendering the *.rst template files
- use the 'run_subprocess' fixture to reduce test boilerplate code

ci
""
- excplicitly use bash as the shell for some job steps


1.6.0 (2022-06-28)
==================

Introducing the *Project Type* Generate Variable. Now you can select what
type of Python Package you intend to develop and the Generation process
shall adjust to produce the desired skeleton and infrastructure accordingly!

Packaged the existing functionality into the `Module` and `Module + CLI`
Project Types.
Added the new `Pytest Plugin` Project Type, designed for developing Pytest
Plugins and Fixtures (see below).

Project Types currently supported:
- Module: a Python Package intended to serve exclusively as a Software Library
- Module + CLI: a Python Package proving a Software Library and an
    "installable" (executable) Command Line Program/Interface (CLI)
- Pytest Plugin: a Python Package intended to providing a Pyetst Plugin (ie with
    a Test Fixture)

Changes
^^^^^^^

feature
"""""""
- add 'project_type' Variable allowing for 'module', 'module+cli' or 'pytest-plugin' Projects
- conditionaly populate 'test' dependencies, ie based on whether there is a cli entrypoint


1.5.2 (2022-06-22)
==================

Development Update fixing the communication between the CI server and the Test
Coverage Hosting Service. It also enable CI tests for the Documentation
side of the project.

Changes
^^^^^^^

ci
""
- install pyenchant on macos using homebrew
- test documentation tests and building command
- upload code coverage data to codecov.io from within the 'test_suite' job


1.5.1 (2022-06-20)
==================

The Update includes improved code Architecture and better Test code Coverage!
Features shorter Unites of Code, more DRY and more Tests.

Changes
^^^^^^^

test
""""
- add bandit tox env for discovering common security issues
- verify commit message, author and email are the expected ones
- git init, increase test code coverage

refactor
""""""""
- reduce code
- centralize subprocess run invocations

ci
""
- enable network-bound tests to trigger integration testing of the `check_pypi` feature


1.5.0 (2022-06-11)
==================

This release focused on improving the code architecture, reducing technical
debt, decoupling components, cleaning code, fixing styling issues.

It also features some updates in the Generated Project, with improved tox envs,
cleaner python scripts and cleaner development tools' configuration files
(such as .pylintrc, pyproject.toml, tox.ini).

Changes
^^^^^^^

feature
"""""""
- document config settings, improve tox envs & scripts

test
""""
- verify Generator can be invoked as python module: `python -m cookiecutter_python`

refactor
""""""""
- dry code per string_sanitizer implementation
- reduce code in cli.py by delegating error handling to the new cli_handlers.py module
- reduce code of parse_version.py script
- abstract input sanitization
- reduce main code
- decouple components
- clean code, satisfy some todos, dry code

ci
""
- use the template's parse_version script to reduce duplicate code


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
