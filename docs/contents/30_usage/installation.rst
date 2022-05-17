
| **Cookiecutter Python Package**, available as source code on github, is also published
| on *pypi.org*.


Install as PyPi package
-----------------------


In virtual environment (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The recommended way of installing any python package, is use a *python virtual environment*.

Open a console (aka terminal) and run:

.. code-block:: shell

  virtualenv env --python=python3
  source env/bin/activate

  pip install cookiecutter-python

  deactivate

  ln -s env/bin/generate-python ~/.local/bin/generate-python

Now the *generate-python* executable should be available (assuming ~/.local/bin is in your PATH)!


For user 
^^^^^^^^

One could also opt for a *user* installation of *cookiecutter-python* package:

.. code-bloack: shell

  python3 -m pip install --user cookiecutter-python


For all users
^^^^^^^^^^^^^

The least recommended way of installing *cookiecutter-python* package is to
*directly* install in the *host* machine:

.. code-bloack: shell

  sudo python3 -m pip install cookiecutter-python

Note the need to invoke using *sudo*, hence not that much recommended.
