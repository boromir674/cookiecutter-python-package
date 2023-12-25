===================
Why this Generator?
===================

*So, why choose this Python Package Generator?*

Robust CLI
==========

| You want an `easy-to-use`, `cross-platform` CLI.

- It offers an **1-click** command, or option for an interactive `wizard`
- **Tested** on **15 different setups**, across multiple `Platforms` and `Python Interpreters`
  - OS: {Ubuntu, MacOS, Windows} x Python: {3.7, 3.8, 3.9, 3.10, 3.11}
- Built on established software, such as *cookiecutter* and *jinja2*

"DevOps": aka Automations and CI/CD
===================================

| You want to focus on your *business logic* and *test cases*, in new Python projects.

- Scaffolded project is one `push` away of running its CI/CD pipeline on Github Actions.
- **Continuous Deployment** on `v*` tags, at `pypi.org`
- **Continuous Deployment**, of Docker images built from your code, on `Docker Hub`
- Designed for `GitOps`, offering various `automations` for various `developer activities`
- Automations offered through a `tox` "front-end", running `same locally, as in CI`
- The pipeline hosts a **Test Workflow** on *Github Actions* CI, designed to *stress-test* your package.
- Stress-Testing, with **Job Matrix** spanning multiple `Python Interpreters`, `Operating Systems`

Approved Tooling
================

| You want the best tools under your belt, for your development lifecycle.

- `tox`, `poetry`, `ruff`, `mypy`, `pytest`, `black`, `isort`, `mkdocs`, `sphinx`

Template Variant
================

You want `poetry`, but what if you want to develop a `pytest plugin`?

- Generate `module`: a Python Distribution, with python API/sdk
  * configured with `poetry` backend
- Generate `module+cli`: a Python Distribution, with a CLI and a python API/sdk
  * configured with `poetry` backend
- Generate `pytest-plugin`: a Python Distribution, designed for a *pytest plugin*
  * configured with `setuptools` backend, as Required by `pytest`!
