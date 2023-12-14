..  This should not show up in the HTML.
    This should not either.
    Content of the 'How to do quick Docs Release Guide'
    As a guide it is a sequence of steps, that one must follow to achieve a goal.
    As a guide, each step's expected resuilt, can be described (soft requirement, but hard on tutorials).
    Where applicable, the effect of each step is described, so user knows what to expect.

    can be used with .. include::

====================================
Streamline **Documentation** Updates
====================================


1.  Branch of off `main` Branch, and checkout your `topical branch` (`tb`).

2.  Create Docs-only changes and commit them to your `tb`.
3.  Push git tag `quick-release`, to trigger the Docs Release Workflow, on the CI

A new PR, is expected to **open** from `tb` to a `dedicated docs` branch,
and automatically **merge** if Docs Build passed on `rtd` CI.

Then, a new PR, is expected to **open** from `dedicated docs` branch to `main`,
with extra commits with Sem Ver Bump, and Changelog updates.

4. Wait for second PR to open, go to github web IU to review it, and merge it.

A new **tag** is expected to be created (on the new main/master commit),
and a `PyPI` distribution will be uploaded, a new Docker Image on Dockerhub,
and a new Github Release will be created.


Workflows References
--------------------

.. Workflow Links to Source Code
.. * Handle quick release , by PR tb --> db
* quick-docs.yaml_ : Listens to `quick-release` git tag, and merges tb --> db, after opening PR.


.. URL links directives, macros

.. _quick-docs.yaml: https://github.com/boromir674/cookiecutter-python-package/blob/docs/.github/workflows/quick-docs.yaml
