
| **Cookiecutter Python Package**, available as source code on github, is also published
| on *pypi.org*.


Install as PyPi package
-----------------------

Installing `cookiecutter-python` with `pip` is the way to go, for getting the
`generate-python` cli onto your machine. Here we demonstrate how to do that using a


In virtual environment (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with any Python Package, it is recommended to install *cookiecutter-python* inside a
python *virtual environment*. You can use any of `virtualenv`, `venv`, `pyenv` of the
tool of your choice. Here we demonstrate, using `virtualenv`, by running the following commands
in a console (aka terminal):

1. Create a virtual environment

  .. code-block:: shell

    virtualenv env --python=python3

Open a console (aka terminal) and run:

2. Activate environment

  .. code-block:: shell

    source env/bin/activate

3. Install `cookiecutter-python`

  .. code-block:: shell

    pip install cookiecutter-python

4. Create symbolic link for the (current) user

  .. code-block:: shell

    ln -s env/bin/generate-python ~/.local/bin/generate-python


Now the *generate-python* executable should be available (assuming ~/.local/bin is in your PATH)!


For user (option 2)
^^^^^^^^^^^^^^^^^^^

One could also opt for a *user* installation of *cookiecutter-python* package:

.. code-block:: shell

  python3 -m pip install --user cookiecutter-python


For all users (option 3)
^^^^^^^^^^^^^^^^^^^^^^^^

The least recommended way of installing *cookiecutter-python* package is to
*directly* install in the *host* machine:

.. code-block:: shell

  sudo python3 -m pip install cookiecutter-python

Note the need to invoke using *sudo*, hence not that much recommended.


Check installation
------------------

| Now the `generate-python` cli should be available!
| You can verify by running the following:

.. code-block:: shell

  generate-python --version
