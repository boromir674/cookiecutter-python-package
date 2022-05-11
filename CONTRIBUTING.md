# Contributing

Thank you for considering reading this guide!
Contributions are welcome :)


* [Types of Contributions](#Types-of-Contributions)
* [Contributor Setup](#Setting-Up-the-Code-for-Local-Development)
* [Contributor Guidelines](#Contributor-Guidelines)
* [Contributor Testing](#Testing-with-tox)
* [Core Committer Guide](#Core-Committer-Guide)


## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs at [https://github.com/boromir674/cookiecutter-python-package/issues](https://github.com/boromir674/cookiecutter-python-package/issues).

Stmbling upon a Bug means encountering different behaviour than the expected/advertised one. When you are reporting a bug, please include the following infromation by filling in [the template](https://github.com/boromir674/cookiecutter-python-package/.github/blob/master/.github/ISSUE_TEMPLATE/bug_report.md).

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* If you can, provide detailed steps to reproduce the bug.
* If you don't have steps to reproduce the bug, just note your observations in as much detail as you can. Questions to start a discussion about the issue are welcome.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it. See [Contributor Setup](#Setting-Up-the-Code-for-Local-Development) to get started.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "please-help" is open to whoever wants to implement it.

Please do not combine multiple feature enhancements into a single pull request.

See [Contributor Setup](#Setting-Up-the-Code-for-Local-Development) to get started.

### Write Documentation

Cookiecutter Python Package could always use more documentation, whether as part of the official Cookiecutter Python Package docs, in docstrings, etc.

If you want to review your changes on the documentation locally, you can do:

```bash
python3 -m pip install --user tox
tox -e live-html
```

This will compile the documentation (into html) and start watching the files for changes, recompiling as you save.
You can open it in your browser at http://127.0.0.1:8000 !

### Submit Feedback

The best way to send feedback is to file an issue at [https://github.com/boromir674/cookiecutter-python-package/issues](https://github.com/boromir674/cookiecutter-python-package/issues).

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Setting Up the Code for Local Development

Here's how to set up `cookiecutter-python-package` for local development.

1. Fork the `cookiecutter-python-package` repo on GitHub.
2. Clone your fork locally:

```bash
git clone git@github.com:boromir674/cookiecutter-python-package.git
```

3. Install your local copy into a virtualenv. Assuming you have virtualenv installed, this is how you set up your fork for local development:

```bash
cd cookiecutter-python-package
virtualenv cookie-pypi --python=python3
source cookie-pypi/bin/activate
pip install -e .
```

4. Create a branch for local development:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

Now you can make your changes locally.

Probably, you should start by writting test case(s) and then the production code.


1. When you're done making changes, check that your changes pass the tests locally.

Please install tox first:

```bash
python3 -m pip install --user tox
```

For a **quick feedback loop** run tests in `dev` setup, against your installed python version:
Assuming you are using python3.8:

```bash
tox -e py38-dev -vv
```

Run all Test Suite under Python3.8 and test against different ways of doing a 'python installation':

```bash
tox -e py38 -vv
```

For more extensive testing, run the Test Suite against multiple python versions if they are found available on the host machine:

```bash
tox -vv
```

For checking against all of our Lint Rules, run:

```bash
tox -e lint
```

For refactoring the code to match all of our Lint Rules, run:

```bash
APPLY_LINT= tox -e lint
```

For checking compliance with Best Practises for Packaging Python code, run:

```bash
tox -e check
```


1. Ensure that your feature or commit is fully covered by tests. Check the coverage report that should be visible on the console when you run tox

You report will be placed to `htmlcov` directory. Please do not include this directory to your commits, accidentally.

1. Commit your changes and push your branch to GitHub:

```bash
git add -p
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```

8. Submit a pull request through the GitHub website.

## Contributor Guidelines

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. The pull request should be contained: if it's too big consider splitting it into smaller pull requests.
3. If the pull request adds functionality, the docs should be updated.
4. The pull request must pass all CI/CD jobs before being ready for review.
5. If one CI/CD job is failing for unrelated reasons you may want to create another PR to fix that first.

### Coding Standards

* Single Responsibility of Units
* Modularity
* Compisition over Inheritance


## Testing with tox

Tox uses pytest under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the [pytest usage docs](http://pytest.org/en/latest/example/index.html).


To run all tests using various versions of python in virtualenvs defined in tox.ini, just run tox:

```bash
tox
```

To run all tests using python 3.8:

```bash
tox -e py38
```

To only run test cases matching the string 'smoke_test', using python 3.8:

```bash
tox -e py38 -k 'smoke_test'
```


## Core Committer Guide

### Vision and Scope

Core committers, use this section to:

* Guide your instinct and decisions as a core committer
* Limit the codebase from growing infinitely

#### Command-Line Accessible

* Provides a command-line utility that creates a Python Package Project
* Easy to use without having to think too hard
* Flexible for more complex use cases
* Easily extensible

#### API Accessible

* Modular API striving for statelessness

#### Extensible

* Modular Design
* Aim for statelessness


#### Fast and Focused

Cookiecutter Python Package is designed to do one thing, and do that one thing very well.

* Cover the important use cases and as little as possible beyond that :)
* Generate Python Package's from the command-line or API, nothing more

#### Inclusive

* Cross-platform and cross-version support

#### Stable

* Aim for high test coverage and covering corner cases
* No pull requests will be accepted that drop test coverage on any platform
* Stable APIs that tool builders can rely on


### Process: Pull Requests

How to prioritize pull requests, from most to least important:

* Fixes for broken tests. Broken means broken on any supported platform or Python version.
* Extra tests to cover corner cases.
* Minor edits to docs.
* Bug fixes.
* Major edits to docs.
* Features.

#### Pull Requests Review Guidelines
- Think carefully about the long-term implications of the change. How will it affect existing projects that are dependent on this? If this is complicated, do we really want to maintain it forever?
- Take the time to get things right, PRs almost always require additional improvements to meet the bar for quality. **Be very strict about quality.**
- When you merge a pull request take care of closing/updating every related issue explaining how they were affected by those changes. Also, remember to add the author to `AUTHORS.md`.

### Process: Issues

If an issue is a bug that needs an urgent fix, mark it for the next patch release.
Then either fix it or mark as please-help.

For other issues: encourage friendly discussion, moderate debate, offer your thoughts.

### Process: Roadmap

The roadmap located [here](https://github.com/boromir674/cookiecutter-python-package/milestones?direction=desc&sort=due_date&state=open)

Due dates are flexible.

### Process: Release:

* Follow semantic versioning. Look at: [http://semver.org](http://semver.org)
