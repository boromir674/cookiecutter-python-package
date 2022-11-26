===================
Why this Generator?
===================

So, why would one opt for this Python Generator?

It is **easy to use**, allowing the generation of a completely fresh new *Python Package Project*,
though a *cli*.

You can immediately have a *ci* infrastructure and multiple platform-agnostic *shell* commands
working out-of-the-box, so you can focus on developing your *business logic* and your *test cases*.

* It allows scaffolding new projects with a **Test Suite** included, designed to run *Test Cases* in **parallel** (across multiple cpu's) for *speed*.
* New Projects come with a **CI pipeline**, that triggers every time code is pushed on the remote.
* Supports generating projects suited for developing a library (*module*), a cli (*module+cli*) or a pytest plugin.
* The pipeline hosts a **Test Workflow** on *Github Actions* CI, designed to *stress-test* your package.
* Generates a *job matrix* that spawns parallel CI jobs based on factors::
  *python versions*
  *operating system* and
  *package installation methods*
* Extensively tested and built on established software, such as *cookiecutter* and *jinja2*.
