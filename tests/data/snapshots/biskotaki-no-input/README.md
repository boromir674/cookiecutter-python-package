# BISKOTAKI GOLD STANDARD

> Project generated from [cookiecutter-python-package](https://github.com/boromir674/cookiecutter-python-package/)

- **Code:** [https://github.com/boromir674/biskotaki](https://github.com/boromir674/biskotaki-gold)  
- **Docs:** [https://biskotaki.readthedocs.io/en/main/](https://biskotaki-gold.readthedocs.io/en/main/)  
- **PyPI:** [https://pypi.org/project/biskotaki/](https://pypi.org/project/biskotaki/)  
- **CI:** [https://github.com/boromir674/biskotaki/actions/](https://github.com/boromir674/biskotaki/actions/)


## Features

1. **biskotakigold** Python package

   - TODO Document a **Great Feature**
   - TODO Document another **Nice Feature**

2. Tested against multiple `platforms` and `python` versions


## Quickstart

> You need to have `Python` installed.

**TLDR**

| Operation \ Method | Pip | Pipx | Docker |
| - | - | - | - |
| Install | `python3 -m pip install biskotaki` | `pipx install biskotaki` | `docker pull boromir674/biskotaki:master` |
| Run | `biskotaki` | `biskotaki` | `docker run -it --rm boromir674/biskotaki:master` |
| Help | `biskotaki --help` | `biskotaki --help` | `docker run -it --rm boromir674/biskotaki:master --help` |

**Step by Step**

1. Install **biskotakigold** `CLI` in your env, with `pip/pipx`.

```sh
pipx install biskotaki
```

2. Run **biskotakigold** `CLI`, with command:

```sh
biskotakigold --help
```

## Development

> Get started

```sh
uv python pin python3.11
uv venv
uv export --no-dev --frozen --extra test -o prod+test.txt
. .venv/bin/activate

uv pip install --no-deps -r prod+test.txt

uv run --active pytest
```

### Notes
> Testing, Documentation Building, Scripts, CI/CD, Static Code Analysis for this project.

1. **Test Suite**, using `pytest`, located in `tests` dir
2. **Parallel Execution** of Unit Tests, on multiple cpu's
3. **Documentation Pages**, hosted on `readthedocs` server, located in `docs` dir
4. **CI/CD Pipeline**, running on `Github Actions`, defined in `.github/`

   a. **Test Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`, `macos-latest`, `windows-latest`
      2. Python Interpreters: `3.8`, `3.9`, `3.10`, `3.11`, `3.12`

   b. **Continuous Deployment**

      `Production`

    1. **Python Distristribution** to `pypi.org`, on `tags` **v***, pushed to `main` branch
    2. **Docker Image** to `Dockerhub`, on every push, with automatic `Image Tagging`

      `Staging`

    1. **Python Distristribution** to `test.pypi.org`, on "pre-release" `tags` **v*-rc**, pushed to `release` branch

5. **Automation**, using `tox`, driven by single `tox.ini` file

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build` python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org` and `test.pypi.org` servers
   d. **Type Check Command**, using `mypy`
   e. **Lint** *Check* and `Apply` commands, using the fast `Ruff` linter, along with `isort` and `black`


## License

> Free software

[//]: # (this is a comment)

- GNU Affero General Public License v3.0
