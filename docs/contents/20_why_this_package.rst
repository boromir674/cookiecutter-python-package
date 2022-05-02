==================
Why this Template?
==================

So, why would one opt for this Template, instead of the many ones available online?

It is **easy to use**, allowing the generation of a completely fresh new *Python Package Project*,
though a *cli*.

You can immediately have a *ci* infrastructure and multiple platform-agnostic *shell* commands
working out-of-the-box, so you can focus on developing your *business logic* and your *test cases*

* It allows scaffolding new projects with a **Test Suite** included, designed to run *Test Cases* in **parallel** (across multiple cpu's) for *speed*.
* New Projects come with a **CI pipeline**, that triggers every time code is pushed on the remote.
* The pipeline hosts a **Test Workflow** (on *Github Actions*), designed to *stress-test* your package on multiple environments:
  Each environment differs from the others in terms of the combined
  *python versions*
  *operating system* and
  *package installation methods*


Apart from the above motivation, *cookiecutter* is a well established templating tool, that uses the robust *jinja2* templating engine.
