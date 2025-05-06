# Why this Generator?

*So, why choose this Python Package Generator?*

## Robust CLI

You want an `easy-to-use`, `cross-platform` CLI.

- It offers a **1-click** command, or an option for an interactive `wizard`.
- **Tested** on **15 different setups**, across multiple `Platforms` and `Python Interpreters`:
  - **OS**: {Ubuntu, MacOS, Windows} X **Python**: {3.7, 3.8, 3.9, 3.10, 3.11, 3.12}
- Built on established software, such as *cookiecutter* and *jinja2*.

## "DevOps": aka Automations and CI/CD

You want to focus on your *business logic* and *test cases* in new Python projects.

- Scaffolded project is **one push** away from triggering its **CI/CD pipeline** on GitHub Actions.
- **Continuous Deployment**, publishing at `pypi.org`, `Docker Hub`, and `Read The Docs`.
- Designed for **GitOps**, supporting various `automated developer activities`.
- **Automations** with the same entry point for both **CI and Local** runs, via `tox`.
- Stress-Testing, with a **Job Matrix** spanning multiple `Python Interpreters` and `Operating Systems`.

## Approved Tooling

You want the best tools under your belt for your development lifecycle.

- `tox`, `poetry`, `ruff`, `mypy`, `pytest`, `black`, `isort`, `mkdocs`, `sphinx`.

## Template Variant

You want `poetry`, but what if you want to develop a `pytest plugin`?

- Generate **Library**: a Python Distribution, offering modules: Python API/SDK.
  - Configured with **poetry** as the build backend and Package Manager.

- Generate **CLI**: a Python Distribution, offering modules and a CLI as an entry point.
  - Configured with **poetry** as the build backend and Package Manager.

- Generate **Pytest Plugin**: a Python Distribution, designed for a *pytest plugin*.
  - Configured with **setuptools** backend, as required by `pytest`!
