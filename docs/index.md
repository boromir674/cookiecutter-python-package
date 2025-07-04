# Welcome to `Cookiecutter Python Package` Documentation!

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/boromir674/cookiecutter-python-package/test.yaml?style=for-the-badge&logo=github%20actions&logoColor=%2365CDCA&label=CI%2FCD&link=https%3A%2F%2Fgithub.com%2Fboromir674%2Fcookiecutter-python-package%2Factions%2Fworkflows%2Ftest.yaml)](https://github.com/boromir674/cookiecutter-python-package/actions/workflows/test.yaml)    [![Read the Docs](https://img.shields.io/readthedocs/python-package-generator?style=for-the-badge&logo=read%20the%20docs&logoColor=%2365CDCA&label=Docs)](https://python-package-generator.readthedocs.io/en/master/)    [![Release Version](https://img.shields.io/pypi/v/cookiecutter_python?style=for-the-badge&logo=pypi&logoColor=%2365CDCA)](https://pypi.org/project/cookiecutter-python/)      [![Coverage](https://img.shields.io/codecov/c/github/boromir674/cookiecutter-python-package/master?style=for-the-badge&logo=codecov&logoColor=%2365CDCA)](https://app.codecov.io/gh/boromir674/cookiecutter-python-package)
[![PyPI Stats](https://img.shields.io/pypi/dm/cookiecutter-python?logoColor=%2365CDCA&logo=pypi&color=%23849ED9)](https://pypistats.org/packages/cookiecutter-python)     [![Maintainability](https://api.codeclimate.com/v1/badges/1d347d7dfaa134fd944e/maintainability)](https://codeclimate.com/github/boromir674/cookiecutter-python-package/maintainability)      [![Tech Debt](https://img.shields.io/codeclimate/tech-debt/boromir674/cookiecutter-python-package)](https://codeclimate.com/github/boromir674/cookiecutter-python-package/)     [![OpenSSF](https://bestpractices.coreinfrastructure.org/projects/5988/badge)](https://bestpractices.coreinfrastructure.org/en/projects/5988)

**Cookiecutter Python Package**, is an open source project, that **Generates** `Open Source Python Projects`!

## A few words

**Goal** of `Cookiecutter Python Package` project is to automate the process of creating the necessary source files to set up and configure the **SDLF** of a new **Python Package**.

**SDLF** --> `Code`, `Tests`, `CI/CD`, `Docs`, `Docker`, `Config Files`

## **`Generator`** process 

Below is a high-level flowchart of the **`Generator`** process (see [Quick-start](#quick-start) below on how to run):

```mermaid
graph

    %% INPUTS to Generator
    subgraph inputs ["INPUT (Optional)"]
        input_things["Project Name
        Package Type
        CI/CD Pipeline Design
        Docs Builder
        ...
        ...
        "]

    end
    
    inputs ==> derive_default

    %% APPLICATION LAYER
    subgraph gen ["Generator"]

        %% INPUTS to Generator
        template>"Template Files"]
        %% gen_params>"Generator Parameters"]

        derive_default["Derive Default Param Values"]    

        prompt["IF Interactive: Prompt User to override Default"]

        Gen["Generator"]

        %% is_interactive -- "No: set Generator Parameters" --> gen_params
        %% prompt -- "set Generator Parameters" --> gen_params
        %% gen_params ===> Gen

        %% is_interactive -- "No: set Generator Parameters" --> Gen
        
        derive_default --> prompt
        prompt -- "Generator Parameters" --> Gen

        template ===> Gen

    end    
    
    Gen ==> out

    %% OUTPUTS of Generator
    subgraph out ["GENERATED FILES"]
        py["Python Modules
        Test Suite
        CI/CD Pipeline
        Documentation Pages
        Dockerfile
        Python Package Metadata
        Lint Config
        "]

    end
```

*Why choose this Python Package Generator?*
:material-information-outline:{ title="Important information" }

<div class="annotate" markdown>

> You get a **ready-to-develop** `Project`, configured to cover the whole **SDLF** (1):

</div>

1.  :man_raising_hand: Software Development Lifecycle

- Structured as Python Package, according to python standards
- Fully-featured CI/CD Pipeline
- Continuous Documentation build for Website
- Modern-standards toolkit
- Stress-tested across multiple platforms and python versions

Read the [Why to use this package](./topics/why_this_package.md) for more motivation 

## :material-bike-fast: Quick-start

**CLI `--help`**

=== "pipx"

    ```shell
    pipx run cookiecutter-python --help
    ```

=== "Docker"

    ```shell
    docker run -it --rm boromir674/generate-python:master --help
    ```


**Generate Project via interactive CLI**

=== "pipx"

    ```shell
    pipx run cookiecutter-python
    ```

=== "Docker"

    ```shell
    docker run -it --rm boromir674/generate-python:master
    ```

## :material-book-open: Documentation

Read about how to use the `cookiecutter-python` package, understand its features
and capabilities.

<div class="grid cards" markdown>


-   :fontawesome-regular-circle-play:{ .lg .middle } __`How-to` Guides__

    ---
    
    `How-to` **Step-by-step Guides**

    [:octicons-arrow-right-24: :material-rocket-launch: `Install`, `Run`, `Use`](./guides/index.md)


-   :material-application-brackets-outline:{ .lg .middle } __API References__

    ---
    [//]: # (link ./reference/CLI.md does not exist yet, it is generate at docs build-time)
    [:octicons-arrow-right-24: :material-console:{ .lg .middle } generate-python CLI](./reference/CLI.md)

    [//]: # (link ./reference/cookiecutter_python.md does not exist yet, it is generate at docs build-time)
    [:octicons-arrow-right-24: :material-language-python: API Refs](./reference/cookiecutter_python)


-   :fontawesome-solid-book-open:{ .lg .middle } __Topics__

    ---

    **Explanations / Topics**

    [:octicons-arrow-right-24: :material-language-python: Architecture ](./topics/arch.md)

    [:octicons-arrow-right-24: :material-generator-portable: Generator Process ](./topics/generator_process.md)


-   :fontawesome-solid-book-open:{ .lg .middle } __Development Topics__

    ---

    **Topics / Explanations** on Development

    [:octicons-arrow-right-24: :material-hammer-screwdriver: Development Topics ](./topics/development/index.md)


</div>
