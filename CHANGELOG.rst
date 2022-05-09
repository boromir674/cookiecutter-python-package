Changelog
=========

0.9.1 (2022-05-09)
------------------

Added some "juicy" 'code badges' in README, to demonstrate the status reported by
the various CI services that this github repository integrates with.

documentation
^^^^^^^^^^^^^
- add badges demonstrating code coverage percentage & code quality reported CI services


0.9.0 (2022-05-09)
------------------

feature
^^^^^^^
- update generated .gitignore
- add lint check and lint apply tox envs in the generated project
- document the project structure, test infra and ci as changelog entry

fix
^^^
- fix the generated tox ini multifactor environments
- add contributing and license rules for generated package

test
^^^^
- skip test cases needing internet connection for default Test Suite execution
- add test case for running without initializing git repository
- define a test case where we run tox for a newly generated project
- 73% code coverage

documentation
^^^^^^^^^^^^^
- document the get_object fixture
- add instructions on how to Check Lint Rules and apply Lint fixes to satisfy them

ci
^^
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
------------------

docs
^^^^
- add CONTRIBUTING.md

dev
^^^
- add configuration for code static analysis with `pylint`
- add configuration for code static analysis with `prospector`

ci
^^
- add type checking all CI Jobs
