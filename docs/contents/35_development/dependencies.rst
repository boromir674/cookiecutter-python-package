===================================
Dependencies to 3rd Party Libraries
===================================

.. Description of what is this Page
Here you can find information about how we derived our software 3rd-party
module dependencies, to ensure diverse environments are compatible with our
`Python Generator`.

Module Dependencies
===================

.. Description of what is this Section
| We set the **allowed Python runtime** versions from 3.8 to 3.12.
| We Stress Test our distribution on all 5 versions in the range, with the goal to:

- allow diverse environments to run our `Python Generator`
- increase the guarantee that our code is **bug-free** on the most common Python versions

This is also a way of saying, sth along the lines of:

- "I believe my code is better to be run on Python 3.8 to 3.12"
- if outside of this range, it might not work, or it might work, but we don't guarantee it

The 3rd-party module dependencies are kept to minimum, and they where chosen
with **criteria:**

- **Single Responsibility** - to keep the codebase clean
- **Small footprint** - to keep the Docker image size small
- **Adoption** - to ensure the libraries are widely adopted
- **Python compatibility** - to ensure diverse environments are compatible with our `Python Generator`

| Dependencies are declared (ie in *pyproject.toml*) and we distinguish the Prod/Main ones from the optional

| Prod Dependencies are declared (ie in `pyproject.toml` file), for 3 main reasons:

- your app code is directly using the 3rd-party module (runtime dependency)
- a 3rd-party module's transient dependency is used by your app code 
- a 3rd-party module's transient dependency was found to have issues for certain versions

    - restricting the compatibility of your app with other 3rd-party modules
    - having a security vulnerability
    - issue can be causing the tests to fail
    - having a bug that affects the functionality of your app

For example, `cookiecutter` is our primary dependency, since our Generator is practically a wrapper around it.

We trust the `cookiecutter` team to deliver their Sem Ver promise. We also trust the `jinja2` team to deliver their Sem Ver promise.

So we first addition of `cookiecutter` (after migration from poetry to uv) we do:

.. code-block:: bash

    uv add 'cookiecutter >=1.0.0, <2.0.0'


.. Subsectoin with name Breakdown of Dependencies
Breakdown of Prod Dependencies
==============================

.. rst table with columns: Name, version Range, Comment, Interface Surface, Reason

.. TODO implement pydeps based solutions that parses number of edges in the depth-1 all-deps graph
.. TODO the we have the ability to continuous track the 3rd-party libs number of imports to aguge on the interfacing surface area
.. TODO with our codebase

questionary | | only used in one module but critical since it handles interactive cli (although I am pretty sure there many aleternatives open-sourced)

| **NOTE:** request-futures is wrapper for concurrent.requests which is high-level interface for async callables
So we can elminate it and use "vanilla async await where needed and event loop managemtn in the code"

**request-futures** | | used in one module but critical since it handles async requests
**requests** is only used by our app, to impoer an exception and catch it. we can also eliminate this probably

click | | we use "3 components" from it: the sdk to declare our CLI, one exception to register in our app exceptions, one "console echo" callable (i guess for the coloring) | it is a trusted piece of software with a large adoption

attrs | | honestly all our classes are in attrs, but it glorifies the Single Responsibility principal, and actual classes are completely intact. | it is a trusted piece of software with a large adoption

yaml | | our prefered lib for yaml (same as cookiecutter uses), only used in one module for "correct initialization of CLI wizard"
if we ant to remove this we use default cli wizard initiaqlization (point;ess since current cookiecutter also uses it and it is yaml lib! (should be "pure" module) )
gitpython | | only used **in one module** in the post gen hook to support optional **git init** ON/Off switch


+------------------+---------------------+--------------------+-------------------------------------------------------------------------------------+
| Name             | Version Range       | Interface Surface  | Reason                                                                              |
+==================+=====================+====================+=====================================================================================+
| ``cookiecutter`` | >=1.0.0, <2.0.0     | big                | We trust that they respect semver, so inside the range there are no backwards       |
|                  |                     |                    | incompatible changes.                                                              |
+------------------+---------------------+--------------------+-------------------------------------------------------------------------------------+
| jinja2  | | small, but important since we use to manually render the cookie context (required in interactive mode by cli wizard       |