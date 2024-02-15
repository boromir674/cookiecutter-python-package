
| Using the cli is as simple as invoking `generate-python` from a console.

You can run the following to see all the available parameters you can control:

.. INLINE TABS ###################

.. tab:: Pipx / Pip

  .. code-block:: shell

    generate-python --help


.. tab:: Docker (linux shell)

  .. Docker #######

  .. code-block:: shell

    docker run -it --rm boromir674/generate-python:master --help

The most common way to generate a new Python Package Project is to run:

.. INLINE TABS ###################

.. tab:: Pipx / Pip

  .. PIPX Installation #######

  .. code-block:: shell

    generate-python

.. tab:: Docker (linux shell)

  .. Docker #######

  .. code-block:: shell

    docker run -it --rm boromir674/generate-python:master

This will prompt you to input some values and create a fresh new Project in the
current directory!

Now, simply `cd` into the generated Project's directory and enjoy some
of the features the generator supplies new projects with!

More on use cases in the next section.
