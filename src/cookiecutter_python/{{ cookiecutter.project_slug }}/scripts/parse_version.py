#!/usr/bin/env python

import os
import re
import sys
import typing as t

# TODO Improve: try using the semantic_version_checker package for semver regex

ExceptionFactory = t.Callable[[str, str, str], Exception]
ClientCallback = t.Callable[[str, str], t.Tuple]

MatchConverter = t.Callable[[t.Match], t.Tuple]
MatchData = t.Union[
    t.Tuple[t.Callable[[t.Match], t.Tuple], str, t.List[t.Any]],
    t.Tuple[t.Callable[[t.Match], t.Tuple], str],
    t.Tuple[t.Callable[[t.Match], t.Tuple]],
]
# 1st item (Callable): takes a Match object and return a tuple of strings
# 2nd item (str): 'method'/'callable attribute' of the 're' python module)
# 3rd item (list): zero or more additional runtime arguments


DEMO_SECTION: str = (
    "[tool.software-release]\nversion_variable = " "src/package_name/__init__.py:__version__"
)
TOML = 'pyproject.toml'


def build_client_callback(data: MatchData, factory: ExceptionFactory) -> ClientCallback:
    if len(data) == 1:
        data = (data[0], 'search', [re.MULTILINE])
    elif len(data) == 2:
        data = (data[0], data[1], [re.MULTILINE])

    def client_callback(file_path: str, regex: str) -> t.Tuple:
        with open(file_path, 'r') as _file:
            contents = _file.read()
        match = getattr(re, data[1])(regex, contents, *data[2])
        if match:
            extracted_tuple = data[0](match)
            return extracted_tuple
        raise factory(file_path, regex, contents)

    return client_callback


# PARSERS

software_release_parser = build_client_callback(
    (lambda match: (match.group(1), match.group(2)),),
    lambda file_path, reg, string: RuntimeError(
        "Expected to find the '[tool.software-release]' section, in "
        f"the '{file_path}' file, with key 'version_variable'.\nFor example:\n"
        f"{DEMO_SECTION}\n indicates that the version string should be looked "
        "up in the src/package_name/__init__.py file and specifically "
        "a '__version__ = 1.2.3' kind of line is expected to be found."
    ),
)


version_file_parser = build_client_callback(
    (lambda match: (match.group(1),),),
    lambda file_path, reg, string: AttributeError(
        "Could not find a match for regex {regex} when applied to:".format(regex=reg)
        + "\n{content}".format(content=string)
    ),
)


def parse_version(software_release_cfg: str) -> str:
    """Detect, parse and return the version (string) from python source code.

    Get the package version (string) provided that the developer has setup
    indication how to find it.

    Reads the [tool.software-release] section found in pyproject.toml and then
    determines where is the actual version string.
    """
    header = r'\[tool\.software-release\]'
    sep = r'[\w\s=/\.:\d]+'  # in some cases accounts for miss-typed characters!
    version_specification = (
        r"version_variable[\ \t]*=[\ \t]*['\"]?([\w\.]+(?:/[\w\.]+)*):(\w+)['\"]?"
    )
    regex = f"{header}{sep}{version_specification}"

    file_name_with_version, version_variable_name = software_release_parser(
        software_release_cfg, regex
    )

    file_with_version_string = os.path.abspath(
        os.path.join(os.path.dirname(software_release_cfg), file_name_with_version)
    )

    if not os.path.isfile(file_with_version_string):
        raise FileNotFoundError(
            f"Path '{file_with_version_string} does not appear to be valid. "
            f"Please go to the '{software_release_cfg}' file, at the"
            " [tool.software-release] section and set the 'version_variable' "
            "key with a valid file path (to look for the version string). "
            f"For example:\n{DEMO_SECTION}\n"
        )

    reg = f'^{version_variable_name}' + r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'
    (version,) = version_file_parser(file_with_version_string, reg)
    return version


def get_arguments(sys_args: t.List[str]):
    if len(sys_args) == 1:  # no input path was given by user, as console arg
        project_dir = os.getcwd()
    if len(sys_args) > 1:
        project_dir = sys_args[1]
    return lambda x: os.path.abspath(os.path.join(project_dir, x))


def main():
    try:
        toml_file: str = get_arguments(sys.argv)(TOML)
        version_string = parse_version(toml_file)
        print(version_string)
    except (RuntimeError, FileNotFoundError, AttributeError) as exception:
        print(exception)
        sys.exit(1)


if __name__ == '__main__':
    main()
