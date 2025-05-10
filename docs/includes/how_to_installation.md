
**Cookiecutter Python Package**, available as *source code* on github, with published

**Distribution** on *pypi.org* **PyPI**, and **Docker Image** on *hub.docker.com* **Registry**.


=== "Install with *pipx*"

    Install in virtual env, and make available globally in your (host) machine.

    ```sh
    pipx install cookiecutter-python
    ```

    Now, the ``generate-python`` executable should be available.


=== "Via Docker"

    Pull the latest Stable image from Docker Hub

    ```sh
    docker pull boromir674/generate-python:master
    ```

    Now, the CLI should be available, via  
    `docker run -it --rm boromir674/generate-python:master`

    !!! Hint
        
        Tag `master` is latest tested stable. Tag `latest` is literally latest pushed (no stability guaranteed)

=== "Install with *pip*, only Linux / MacOS"

    Install in virtual env

    ```sh
    virtualenv env --python=python3
    source env/bin/activate

    pip install cookiecutter-python
    ```

    Make available to current user

    ```sh
    ln -s env/bin/generate-python ~/.local/bin/generate-python
    ```

Now, the ``generate-python`` executable should be available (assuming ~/.local/bin is in your PATH).

!!! Hint

    All methods shown above Download Latest Stable Releases, either from pypi or docker


### Verify Installation

You can verify by running the following:

```sh
generate-python --version
```
