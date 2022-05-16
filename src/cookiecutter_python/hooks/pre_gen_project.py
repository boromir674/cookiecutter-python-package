import asyncio
import sys

from software_patterns import SubclassRegistry

from cookiecutter_python.backend.check_pypi_handler import available_on_pypi
from cookiecutter_python.backend.input_sanitization import (
    InputValueError,
    build_input_verification,
)


def get_request():
    # Templated Variables should be centralized here for easier inspection
    # Also, this makes static code analyzers to avoid issues with syntax errors
    # due to the templated (dynamically injected) code in this file

    # the name the client code should use to import the generated package/module
    module_name = '{{ cookiecutter.pkg_name }}'

    return type(
        'PreGenProjectRequest',
        (),
        {
            'module_name': module_name,
            'pypi_package': module_name.replace('_', '-'),
            'package_version_string': '{{ cookiecutter.version }}',
        },
    )


verify_templated_module_name = build_input_verification(
    'module-name',
)

verify_templated_semantic_version = build_input_verification(
    'semantic-version',
)


def input_sanitization(request):
    # CHECK Package Name
    try:
        verify_templated_module_name(request.module_name)
    except InputValueError as error:
        raise InputValueError(
            'ERROR: %s is not a valid Python module name!', request.module_name
        ) from error

    # CHECK Version
    try:
        verify_templated_semantic_version(request.package_version_string)
    except InputValueError as error:
        raise InputValueError(
            'ERROR: %s is not a valid Semantic Version!', request.package_version_string
        ) from error


# Synchronous Task

def hook_main(request):
    try:
        input_sanitization(request)
    except InputValueError as error:
        print(error)
        return 1
    print("Sanitized Input Variables :)")
    return 0


# Asynchronous Tasks

class Task(metaclass=SubclassRegistry):
    """Asynchronous Task.

    Each subclass must implement an async run method that can include
    both typical synchronous statements and "awaited" async statements.
    """

    pass


# Async Task 1


@Task.register_as_subclass('main')
class MainTask(Task):
    async def run(self, *args):
        return hook_main(*args)


# Async Task 2

@Task.register_as_subclass('is-on-pypi')
class PypiTask(Task):
    async def run(self, *args):
        return available_on_pypi(*args)


# ASYNC Infra
class WorkDesign:
    def __init__(self, data):
        self.data = data


class TaskDesign:
    def __init__(self, name: str, work: WorkDesign) -> None:
        self.name = name
        self.work = work

    def to_asyncio_task(self, work_queue):
        return asyncio.create_task(task(self.name, work_queue))


async def task(name, work_queue):
    while not work_queue.empty():
        work = await work_queue.get()
        task_instance = Task.create(name)
        return await task_instance.run(work.data)


async def async_main(request):
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    tasks = [
        TaskDesign(name, WorkDesign(work))
        for name, work in (
            ('is-on-pypi', request.pypi_package),
            ('main', request),
        )
    ]
    # Put some work in the queue
    for task_design in tasks:
        await work_queue.put(task_design.work)

    # Run the tasks
    is_on_pypi, exit_code = await asyncio.gather(
        *[task.to_asyncio_task(work_queue) for task in tasks]
    )

    return exit_code


# TODO Remove ASYNC SWITCH
async_on = 0


def _main():
    request = get_request()
    if async_on:
        return asyncio.run(async_main(request))
    return hook_main(request)


# MAIN


def main():
    exit_code = _main()
    if exit_code == 0:
        print('Finished Pre Gen Hook :)')
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
