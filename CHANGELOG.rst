Changelog
=========

0.9.1 (2022-05-09)
------------------

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
^^
Apply the same CI additions as the ones added for the Template project (see above)!
Namely:

- extra `checks` in the `Test Jobs`
- `integration` with the `codecov.io` Code Coverage hosting service

documentation
^^^^^^^^^^^^^
Add some "juicy" **code badges** in `README`, to demonstrate the `status` reported by
the various `CI services` that this repository integrates with.

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
