===================================
Generate New Python Package Project
===================================

| The most common way to generate a new Python Package Project (in the current working directory),
| is to invoke the *cookiecutter* cli (while supplying the necessary initial information when prompted)
| and provide this Template as input.

Open a console (ie terminal) and run: 

.. code-block:: shell
  
  # Get Template
  git clone git@github.com/boromir674/cookiecutter-python-package.git

  # Install cookiecutter if you haven't
  python -m pip3 install cookiecutter 

  # Generate a new Python Package Project locally
  cookiecutter cookiecutter-python-package/src/cookiecutter_python


.. include:: installation.rst
