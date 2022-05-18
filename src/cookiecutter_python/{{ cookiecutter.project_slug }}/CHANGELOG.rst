=========
Changelog
=========

0.0.1 ({{ cookiecutter.release_date }})
=======================================

| This is the first ever release of the **{{ cookiecutter.pkg_name }}** Python Package.
| The package is open source and is part of the **{{ cookiecutter.project_name }}** Project.
| The project is hosted in a public repository on github at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
| The project was scaffolded using the `Cookiecutter Python Package`_ (cookiecutter) Template at https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

| Scaffolding included:

- **CI Pipeline** running on Github Actions at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}/actions
  - `Test Workflow` running a multi-factor **Build Matrix** spanning different `platform`'s and `python version`'s
    1. Platforms: `ubuntu-latest`, `macos-latest`
    2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`

- Automated **Test Suite** with parallel Test execution across multiple cpus.
  - Code Coverage
- **Automation** in a 'make' like fashion, using **tox**
  - Seamless `Lint`, `Type Check`, `Build` and `Deploy` *operations*


.. LINKS

.. _Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/master/
