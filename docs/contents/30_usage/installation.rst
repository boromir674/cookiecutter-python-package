
| **Cookiecutter Python Package**, available as *source code* on github, with published
| **Distribution** on *pypi.org* **PyPI**, and **Docker Image** on *hub.docker.com* **Registry**.

.. PIPX Installation #######

.. tab:: Install with *pipx*

  Install in virtual env, and make available globally in your (host) machine.

  .. code-block:: shell

   pipx install cookiecutter-python

  Now, the ``generate-python`` executable should be available.

  .. DOCKER Installation #######

.. tab:: Via Docker

  Pull the latest Stable image from Docker Hub

  .. code-block:: shell

    docker pull boromir674/generate-python:master

  | Now, the CLI should be available, via
  | ``docker run -it --rm boromir674/generate-python:master``

  .. Hint:: Not to be confused with the 'latest' (channel) image tag advertised by dockerhub, which my no means promises to contain a stable release.
  .. Hint:: We promise stable releases on **'master'** tag, since on git, 'all tagged production releases are on 'master' branch.
      They are the same to correspond to PyPI Distributions as well.

  .. PIP Installation #######

.. tab:: Install with *pip*, only Linux / MacOS

  Install in virtual env

  .. code-block:: shell

    virtualenv env --python=python3
    source env/bin/activate

    pip install cookiecutter-python

  Make available to current user

  .. code-block:: shell

    ln -s env/bin/generate-python ~/.local/bin/generate-python

  Now, the ``generate-python`` executable should be available (assuming ~/.local/bin is in your PATH).


Check installation
~~~~~~~~~~~~~~~~~~

| You can verify by running the following:

.. code-block:: shell

  generate-python --version

.. HINT All methods Download Stable Releases, either pypi or docker #######

.. Hint:: All methods demonstrated for **getting the CLI**, *download* the **Latest Stable** (Release).
