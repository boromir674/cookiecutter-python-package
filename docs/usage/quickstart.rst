**********
Quickstart
**********

| The most common case is to generate a new Python Package Project (in the current working directory),
| while providing the necessary initial information at runtime though the cli parameters.

Open a console (ie terminal) and run: 

.. code-block:: shell
  
  # Get Template
  git clone git@github.com/boromir674/cookiecutter-python-package.git

  # Install cookiecutter if you haven't
  python -m pip3 install cookiecutter 

  # Generate a new Python Package Project locally
  cookiecutter cookiecutter-python-package/src/cookiecutter_python
