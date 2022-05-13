import json
import logging
import re
import sys
from typing import Pattern
import asyncio
from codetiming import Timer
from requests_futures.sessions import FuturesSession

from software_patterns import SubclassRegistry

from cookiecutter_python.backend.check_pypi_handler import available_on_pypi, handle_availability


logger = logging.getLogger(__name__)


session = FuturesSession()

async def is_on_pypi(package_name: str):
    # first request is started in background
    future_one = session.get(f'https://pypi.org/project/{package_name}')
    return future_one.result().status_code == 200


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


def verify_regex_and_log(message_getter):
    def _verify_regex_and_log(regex: Pattern, string: str):
        if not regex.match(string):
            msg = "RegEx Miss Match Error"
            logger.error(message_getter(msg, regex, string))
            raise RegExMissMatchError(msg)

    return _verify_regex_and_log


def verify_input_with_regex_callback(verify_callback, exception_message=None):
    def verify_input_with_regex(regex: Pattern, string: str):
        try:
            verify_callback(regex, string)
        except RegExMissMatchError as not_matching_regex:
            raise InputValueError(
                exception_message if exception_message else ''
            ) from not_matching_regex

    return verify_input_with_regex


def get_verify_callback(error_message, log_message_getter):
    def _verify_regex(regex: Pattern, string: str):
        verify_input_with_regex_callback(
            verify_regex_and_log(log_message_getter), exception_message=error_message
        )(regex, string)

    return _verify_regex


def verify_templated_semantic_version(version: str):
    REGEX = re.compile(
        r'^(?P<major>0|[1-9]\d*)'
        r'\.'
        r'(?P<minor>0|[1-9]\d*)'
        r'\.'
        r'(?P<patch>0|[1-9]\d*)'
        r'(?:-'
        r'(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+'
        r'(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    )

    def log_message(error, regex, string):
        return (
            "%s: %s",
            str(error),
            json.dumps(
                {
                    'semver_regex': str(regex.pattern),
                    'version_string': str(string),
                }
            ),
        )

    get_verify_callback(
        error_message='Expected a Semantic Version value',
        log_message_getter=log_message,
    )(REGEX, version)


def verify_templated_module_name(module: str):
    REGEX = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]+$')

    def log_message(error, regex, module):
        return (
            "%s: %s",
            str(error),
            json.dumps(
                {
                    'module_name_regex': str(regex.pattern),
                    'module_name': str(module),
                }
            ),
        )

    get_verify_callback(
        error_message='Expected a valid Python Module name value',
        log_message_getter=log_message,
    )(REGEX, module)


def hook_main(request):
    # CHECK Package Name
    try:
        verify_templated_module_name(request.module_name)
    except InputValueError:
        print('ERROR: %s is not a valid Python module name!' % request.module_name)
        return request, 1

    # CHECK Version
    try:
        verify_templated_semantic_version(request.package_version_string)
    except InputValueError:
        print('ERROR: %s is not a valid Semantic Version!' % request.package_version_string)
        return request, 1

    # CHECK if given package name is already registerered on pypi
    available_on_pypi(request.pypi_package)  # does not raise an exception
    
    print("Pre Gen Hook: Finished :)")
    return request, 0


def _main():
    request = get_request()
    # SYNC
    return hook_main(request)[1]
    # ASYNC
    # return asyncio.run(async_main(request))


async def _async_main(request):
    asyncio.sleep(0)
    # CHECK Package Name
    try:
        verify_templated_module_name(request.module_name)
    except InputValueError:
        print('ERROR: %s is not a valid Python module name!' % request.module_name)
        return 1

    # CHECK Version
    try:
        verify_templated_semantic_version(request.package_version_string)
    except InputValueError:
        print('ERROR: %s is not a valid Semantic Version!' % request.package_version_string)
        return 1
    
    print("Pre Gen Hook: Finished :)")
    return 0


@Task.register_as_subclass('main')
class MainTask(Task):

    async def run(self, *args):
        return await _async_main(*args)

@Task.register_as_subclass('is-on-pypi')
class PypiTask:

    async def run(self, *args):
        return await is_on_pypi(*args)


def main():
    sys.exit(_main())



class RegExMissMatchError(Exception):
    pass


class InputValueError(Exception):
    pass

class WorkDesign:
    def __init__(self, data):
        self.data = data


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: " + "{:.1f}")
    while not work_queue.empty():
        work = await work_queue.get()
        print(f"Task {name} running")
        task_instance = Task.create(name)
        timer.start()
        res = await task_instance.run(work.data)
        timer.stop()
        return res


async def async_main(request):
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [request, request.pypi_package]:
        await work_queue.put(WorkDesign(work))

    # Run the tasks
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        exit_code, (request, is_on_pypi) = await asyncio.gather(
            asyncio.create_task(task("main", work_queue)),
            asyncio.create_task(task("is-on-pypi", work_queue)),
        )

        handle_availability(
            registered_on_pypi=is_on_pypi,
            package_name=request.pypi_package
        )
    return exit_code


if __name__ == "__main__":
    main()
    # asyncio.run(async_main())
