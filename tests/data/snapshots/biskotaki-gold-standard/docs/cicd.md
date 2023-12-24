---
tags:
  - CICD
---

## CI/CD Pipeline, publishing to Docker and PyPI

About the `CI/CD Pipeline`, which is part the Project's Source Repository.

The `Pipeline` is implemented as a `Github Actions` **Workflow**, and is part
of the Projects Source Repository: [.github/workflows/test.yaml](https://github.com/boromir674/biskotaki-gold/blob/main/.github/workflows/test.yaml)

It is designed with `"DevOps"` good-practices, and some of its features include:

- Running the Test Suite on different `Platforms`: Ubuntu, MacOs, Windows
- Running the Test Suite on different `Python Versions`, ie 3.8, 3.10, 3.11
- **Stress Testing**, against the Test Suite, factoring `Platforms` and `Python Version`s
- Automatically `Publishing to PyPI`, on `Release` events
- Automatically `Publishing to Dockerhub`, on *branches* and *tags*
- `Static Code Analysis`, with tools such as `Mypy`, `Ruff`, `Black`, and `Isort`
- Visualizing Code, in SVG, as a `Graph` of Python Imports


### Variables to provide for `var` context

Flow Chart, of Jobs Dependencies in the Pipeline.  
Here only `Caller` Jobs are shown; no `Called` (aka downstream) Workflows are shown.

[link]: https://github.com/boromir674/biskotaki-gold/blob/main/.github/workflows/test.yaml "Online Config File"

**config: [.github/workflows/test.yaml][link]**


{% include 'cicd_mermaid.md' %}
