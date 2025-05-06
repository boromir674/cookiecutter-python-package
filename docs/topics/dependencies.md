# Dependencies to 3rd Party Libraries

Here you can find information about how we derived our software 3rd-party module dependencies, to ensure diverse environments are compatible with our `Python Generator`.

## Module Dependencies

[//]: # (this is a comment)

We set the **allowed Python runtime** versions from 3.8 to 3.12.  
We Stress Test our distribution on all 5 versions in the range, with the goal to:

- Allow diverse environments to run our `Python Generator`
- Increase the guarantee that our code is **bug-free** on the most common Python versions

This is also a way of saying something along the lines of:

- "I believe my code is better to be run on Python 3.8 to 3.12"
- If outside of this range, it might not work, or it might work, but we don't guarantee it

The 3rd-party module dependencies are kept to a minimum, and they were chosen with the following **criteria**:

- **Single Responsibility** - To keep the codebase clean
- **Small footprint** - To keep the Docker image size small
- **Adoption** - To ensure the libraries are widely adopted
- **Python compatibility** - To ensure diverse environments are compatible with our `Python Generator`

Dependencies are declared (e.g., in *pyproject.toml*), and we distinguish the Prod/Main ones from the optional ones.

### Prod Dependencies

Prod Dependencies are declared (e.g., in the `pyproject.toml` file), for 3 main reasons:

1. Your app code is directly using the 3rd-party module (runtime dependency).
2. A 3rd-party module's transient dependency is used by your app code.
3. A 3rd-party module's transient dependency was found to have issues for certain versions:
    - Restricting the compatibility of your app with other 3rd-party modules
    - Having a security vulnerability
    - Causing the tests to fail
    - Having a bug that affects the functionality of your app

For example, `cookiecutter` is our primary dependency, since our Generator is practically a wrapper around it.

We trust the `cookiecutter` team to deliver their SemVer promise. We also trust the `jinja2` team to deliver their SemVer promise.

So, for the first addition of `cookiecutter` (after migration from poetry to uv), we do:

```sh
uv add 'cookiecutter >=1.0.0, <2.0.0'
```

## Breakdown of Prod Dependencies

- **questionary**: Only used in one module but critical since it handles interactive CLI (although there are many open-sourced alternatives).
- **request-futures**: A wrapper for `concurrent.requests`, which is a high-level interface for async callables.  
  We can eliminate it and use "vanilla async/await" where needed and manage the event loop in the code.
- **requests**: Only used by our app to import an exception and catch it. This can probably be eliminated.
- **click**: We use 3 components from it:
  - The SDK to declare our CLI
  - One exception to register in our app exceptions
  - One "console echo" callable (for coloring)  
  It is a trusted piece of software with large adoption.
- **attrs**: All our classes use `attrs`. It glorifies the Single Responsibility Principle, and actual classes are completely intact.  
  It is a trusted piece of software with large adoption.
- **yaml**: Our preferred library for YAML (same as `cookiecutter` uses). Only used in one module for "correct initialization of CLI wizard."  
  If we want to remove this, we can use the default CLI wizard initialization (pointless since `cookiecutter` also uses it).
- **gitpython**: Only used **in one module** in the post-gen hook to support the optional **git init** ON/OFF switch.

### Dependency Table

| Name             | Version Range       | Interface Surface  | Reason                                                                              |
|-------------------|---------------------|--------------------|-------------------------------------------------------------------------------------|
| `cookiecutter`    | >=1.0.0, <2.0.0     | Big                | We trust that they respect SemVer, so inside the range there are no backwards incompatible changes.       |
| `jinja2`          |                     | Small              | Important since we use it to manually render the cookie context (required in interactive mode by CLI wizard). |

