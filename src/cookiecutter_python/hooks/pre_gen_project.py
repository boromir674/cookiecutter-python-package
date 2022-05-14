import json
import logging
import re
import sys
from typing import Pattern
import asyncio
from codetiming import Timer
from requests_futures.sessions import FuturesSession
from requests.exceptions import ConnectionError
# from cookiecutter_python.backend.check_pypi import is_registered_on_pypi
from software_patterns import SubclassRegistry
from cookiecutter_python.backend.input_sanitization import InputValueError

from cookiecutter_python.backend.check_pypi_handler import available_on_pypi, handle_availability
from cookiecutter_python.backend.input_sanitization import get_verify_callback
from cookiecutter_python.backend.input_sanitization import build_input_verification


logger = logging.getLogger(__name__)


session = FuturesSession()

async def is_on_pypi(package_name: str):
    # first request is started in background
    try:
        # exists_on_pypi = is_registered_on_pypi(package_name)
        future_one = session.get(f'https://pypi.org/project/{package_name}')
        exists_on_pypi = future_one.result().status_code == 200
        # await asyncio.sleep(4)
        handle_availability(
            registered_on_pypi=exists_on_pypi,
            package_name=package_name,
        )
    except ConnectionError as error:  # ie network/wifi not working  
        print(error, file=sys.stderr)
        print("Could not establish connection to pypi.")
        print(f"Could not determine whether the selected pypi name '{package_name}' is already taken.")


class Task(metaclass=SubclassRegistry):
    pass


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
        raise InputValueError('ERROR: %s is not a valid Python module name!', request.module_name) from error

    # CHECK Version
    try:
        verify_templated_semantic_version(request.package_version_string)
    except InputValueError as error:
        raise InputValueError('ERROR: %s is not a valid Semantic Version!', request.package_version_string) from error
    print("Sanitized Input Variables :)")
    return 0



# Synchronous Task

def hook_main(request):
    try:
        input_sanitization(request)
    except InputValueError as error:
        print(error)
        return 1

    # CHECK if given package name is already registered on pypi
    timer = Timer(text="\nPyPi Check elapsed time: " + "{:.5f}")
    timer.start()
    available_on_pypi(request.pypi_package)  # does not raise an exception
    timer.stop()

    return 0


# Asynchronous Tasks

@Task.register_as_subclass('main')
class MainTask(Task):

    async def run(self, *args):
        return await async_input_sanitization(*args)

# Async Task 2
@Task.register_as_subclass('is-on-pypi')
class PypiTask:

    async def run(self, *args):
        return await is_on_pypi(*args)

# ASYNC Infra

async def async_input_sanitization(request):
    return input_sanitization(request)

class WorkDesign:
    def __init__(self, data):
        self.data = data


async def task(name, work_queue):
    # timer = Timer(text=f"Task {name} elapsed time: " + "{:.5f}")
    while not work_queue.empty():
        work = await work_queue.get()
        # print(f"Task {name} running")
        task_instance = Task.create(name)
        # timer.start()
        try:
            res = await task_instance.run(work.data)
        except InputValueError as error:
            print(error)
            res = 1
            # sys.exit(1)
        # timer.stop()
        return res


async def async_main(request):
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [request.pypi_package, request]:
        await work_queue.put(WorkDesign(work))

    # Run the tasks
    # with Timer(text="\nTotal elapsed time: {:.5f}"):
    is_on_pypi, exit_code = await asyncio.gather(
        asyncio.create_task(task("is-on-pypi", work_queue)),
        asyncio.create_task(task("main", work_queue)),
    )

    return exit_code


# TODO Remove ASYNC SWITCH
async_on = 1

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
    with Timer(text="Total elapsed time: {:.5f}"):
        main()
