# Python Package Generator

[![Build Status](https://img.shields.io/github/actions/workflow/status/boromir674/cookiecutter-python-package/test.yaml?link=https%3A%2F%2Fgithub.com%2Fboromir674%2Fcookiecutter-python-package%2Factions%2Fworkflows%2Ftest.yaml%3Fquery%3Dbranch%253Amaster)](https://github.com/boromir674/cookiecutter-python-package/actions/workflows/test.yaml?query=branch%3Amaster) [![Coverage](https://img.shields.io/codecov/c/github/boromir674/cookiecutter-python-package/master?logo=codecov)](https://app.codecov.io/gh/boromir674/cookiecutter-python-package) [![Docs](https://img.shields.io/readthedocs/python-package-generator/master?logo=readthedocs&logoColor=lightblue)](https://python-package-generator.readthedocs.io/en/master/) [![Maintainability](https://api.codeclimate.com/v1/badges/1d347d7dfaa134fd944e/maintainability)](https://codeclimate.com/github/boromir674/cookiecutter-python-package/maintainability)
[![Release Version](https://img.shields.io/pypi/v/cookiecutter_python)](https://pypi.org/project/cookiecutter-python/) [![Wheel](https://img.shields.io/pypi/wheel/cookiecutter-python?color=green&label=wheel)](https://pypi.org/project/cookiecutter-python) [![Tech Debt](https://img.shields.io/codeclimate/tech-debt/boromir674/cookiecutter-python-package)](https://codeclimate.com/github/boromir674/cookiecutter-python-package/) [![Codacy](https://app.codacy.com/project/badge/Grade/5be4a55ff1d34b98b491dc05e030f2d7)](https://app.codacy.com/gh/boromir674/cookiecutter-python-package/dashboard?utm_source=github.com&utm_medium=referral&utm_content=boromir674/cookiecutter-python-package&utm_campaign=Badge_Grade)
[![Supported Versions](https://img.shields.io/pypi/pyversions/cookiecutter-python?color=blue&label=python&logo=python&logoColor=%23ccccff)](https://pypi.org/project/cookiecutter-python)
[![PyPI Stats](https://img.shields.io/pypi/dm/cookiecutter-python?logo=pypi&logoColor=%23849ED9&color=%23849ED9)](https://pypistats.org/packages/cookiecutter-python) [![Commits Since Tag](https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/v2.5.10/master?color=blue&logo=github)](https://github.com/boromir674/cookiecutter-python-package/compare/v2.5.10..master) [![Commits Since Release](https://img.shields.io/github/commits-since/boromir674/cookiecutter-python-package/latest?color=blue&logo=semver&sort=semver)](https://github.com/boromir674/cookiecutter-python-package/releases)
[![License](https://img.shields.io/github/license/boromir674/cookiecutter-python-package)](https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE) [![OpenSSF](https://bestpractices.coreinfrastructure.org/projects/5988/badge)](https://bestpractices.coreinfrastructure.org/en/projects/5988) [![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

  
**Create** Python Projects swiftly, and enjoy **streamlined "DevOps"** using a powerful **CI/CD Pipeline.**  

> **Documentation available at https://python-package-generator.readthedocs.io/.**

[//]: # (TODO add a pre-recorded video embed to demo what this does!)

## What's included?

- **Generator** of **Python Project** (see [Quickstart](#quickstart)), with **CLI** for **Linux**, **MacOS**, and **Windows**
- **Option** to Generate Python Package designed as `module`, `module+cli`, or `pytest-plugin`!
- Scaffold over **24 files**, from [Template](#template), to have a `ready-to-develop` **Project equipped** with:
  - Fully-featured **CI/CD Pipeline**, running on [Github Actions](https://github.com/boromir674/cookiecutter-python-package/actions), defined in `.github/`
  - **Continuous Delivery** to *PyPI* (i.e. [pypi.org](https://pypi.org/), [test.pypi.org](https://test.pypi.org/)) and *Dockerhub*
  - **Continuous Integration**, with **Test Suite** running [pytest](https://docs.pytest.org/en/7.1.x/), located in the `tests` dir
  - **Continuous Documentation**, building with `mkdocs` or `sphinx`, and hosting on `readthedocs`, located in the `docs` dir
  - **Static Type Checking**, using [mypy](https://mypy.readthedocs.io/en/stable/)
  - **Lint** *Check* and `Apply` commands, using the fast [Ruff](https://docs.astral.sh/ruff/) linter, along with standard [isort](https://pycqa.github.io/isort/), and [black](https://black.readthedocs.io/en/stable/)
  - **Build Command**, using the [build](https://github.com/pypa/build) python package


## What to expect?

You can be up and running with a new Python Package, and run workflows on Github Actions, such as:

![CI Pipeline](https://raw.githubusercontent.com/boromir674/cookiecutter-python-package/master/docs/assets/CICD-Pipe.png)

1. **CI Pipeline**, running on [Github Actions](https://github.com/boromir674/cookiecutter-python-package/actions), defined in `.github/`
   - **Job Matrix**, spanning different `platform`s and `python version`s:
     - Platforms: `ubuntu-latest`, `macos-latest`
     - Python Interpreters: `3.8`, `3.9`, `3.10`, `3.11`, `3.12`
   - **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`
   - **Artifact** store of **Source** and **Wheel** Distributions, factoring Platform and Python Version

### Auto Generated Sample Package **Biskotaki**

Check the [**Biskotaki** *Python Package Project* on github](https://github.com/boromir674/biskotaki), which is Continuously generated by this CLI, for a taste of how a project looks and the files this Template can generate!

- **Source Code** hosted on *Github* at <https://github.com/boromir674/biskotaki>  
- **Python Package** hosted on *pypi.org* at <https://pypi.org/project/biskotaki/>  
- **Live Documentation** hosted on *readthedocs* at https://python-package-generator.readthedocs.io/  
- **CI Pipeline** hosted on *Github Actions* at <https://github.com/boromir674/biskotaki/actions>


## Quickstart

To **install** the latest `Generator` in your environment, run:

``` shell
pip install cookiecutter-python
```

The `generate-python` CLI should become available in your environment.

Next, create a file, let's call it `gen-config.yml`, with the following
content:

``` yaml
default_context:
    project_name: Demo Generated Project
    project_slug: demo-project
    project_type: module+cli
    full_name: John Doe
    email: john.doe@something.org
    github_username: john-doe
    project_short_description: 'Demo Generated Project Description'
    initialize_git_repo: no
    interpreters: {"supported-interpreters": ["3.8", "3.9", "3.10", "3.11"]}
```

To **generate** a Python Package Project, run:

``` sh
mkdir gen-demo-dir
cd gen-demo-dir

generate-python --config-file ../gen-config.yml --no-input
```

Now, you should have generated a new Project for a Python Package, based on the [Template](https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python)!

The Project should be located in the newly created `demo-generated-project` directory.

To leverage all out-of-the-box development operations (ie scripts), install [tox](https://tox.wiki/en/latest/):

``` shell
python3 -m pip install --user 'tox<4'
```

To verify tox available in your environment, run: `tox --version`

```sh
cd demo-project
```

To run the **Test Suite**, run:

``` shell
tox -e dev
```

All Tests should pass, and you should see a **coverage** report!

To run **Type Checking** against the Source Code, run:

``` shell
tox -e type
```

All Type Checks should pass!

To setup a Git Repository, run:

``` shell
git init
git add .
git checkout -b main
git commit -m "Initial commit"
```

To setup a Remote Repository, run for example:

``` shell
git remote add origin <remote-repository-url>
git push -u origin main
```

To trigger the CI/CD Pipeline, run:

``` shell
git push
```

Navigate to your github.com/username/your-repo/actions page, to see the
CI Pipeline running!

Develop your package's **Source Code** (business logic) inside `src/my_great_python_package` :)  
Develop your package's **Test Suite** (ie unit-tests, integration tests, etc) inside `tests` dir :-)

Read the Documentation's [Use Cases](https://python-package-generator.readthedocs.io/en/master/contents/30_usage/index.html#new-python-package-use-cases) section for more on how to leverage your generated Python Package features.

### Next Steps

To prepare for an Open Source Project Development Lifecycle, you should visit the following websites:

-   PyPI, test.pypi.org, Dockerhub, and Read the Docs, for setting up Release and Documentation Pipelines
-   github.com/your-account to configure Actions, through the web UI
-   Codecov, Codacy, and Codeclimate, for setting up Automated Code Quality, with CI Pipelines
-   <https://www.bestpractices.dev/> for registering your Project for OpenSSF Best Practices Badge

**Happy Developing!**

## License

> [GNU Affero General Public License v3.0](https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE)

[![GitHub](https://img.shields.io/github/license/boromir674/cookiecutter-python-package)](https://github.com/boromir674/cookiecutter-python-package/blob/master/LICENSE)


### Free/Libre and Open Source Software (FLOSS)

[![OpenSSF](https://bestpractices.coreinfrastructure.org/projects/5988/badge)](https://bestpractices.coreinfrastructure.org/en/projects/5988)
