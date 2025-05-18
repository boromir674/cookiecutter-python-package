# Changelog


## 0.1.0 (2025-05-18)

> This is the **first ever release** of the `open source` **Biskotaki** Project and the included **biskotaki** Python Package.

The project is hosted in a public repository on github at https://github.com/boromir674/biskotaki

The project was scaffolded using the [`Cookiecutter Python Package`](https://python-package-generator.readthedocs.io/en/master/) **Python Project Generator**

- Template at https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

### Scaffolding

- Fast **CI/CD Pipeline** running on Github Actions at https://github.com/boromir674/biskotaki/actions

  - `Test Workflow` running a multi-factor **Build Matrix** spanning different `platform`'s and `python version`'s
    1. Platform OS: `ubuntu-latest`, `macos-latest`
    2. Python Runtime versions: `3.8`, `3.9`, `3.10`, `3.11`, `3.12`

  - **Continuous Delivery** to `Dockerhub`
  - **Continuous Delivery** to `PyPI`
  
  - **Continuous Documentation**, with `mkdocs` and `readthedocs` integration
  - **Automated QA**: `Type Check`, `Dev Sec Ops`, `Lint`

- **Test Suite** with automated parallel Test execution across multiple cpus.
  - Code Coverage, measuring and Uploading
