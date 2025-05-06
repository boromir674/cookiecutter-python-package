
> Using the cli is as simple as invoking `generate-python` from a console.

You can run the following to see all the available parameters you can control:


=== "Pipx / Pip"

    ```sh
    generate-python --help
    ```

=== "Docker"

    ```sh
    docker run -it --rm boromir674/generate-python:master --help
    ```

The most common way to generate a new Python Package Project is to run:


=== "Pipx / Pip"
    
    ```sh
    generate-python
    ```

=== "Docker (linux shell)"

    ```sh
    docker run -it --rm boromir674/generate-python:master
    ```

This will prompt you to input some values and create a fresh new Project in the current directory!

Now, simply `cd` into the generated Project's directory and enjoy some of the features the generator supplies new projects with!

More on use cases in the next section.
