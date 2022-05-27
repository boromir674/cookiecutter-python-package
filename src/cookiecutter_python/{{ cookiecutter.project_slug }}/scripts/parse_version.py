#!/usr/bin/env python

import os
import re
import sys
import typing as t

# TODO Improve: try using the semantic_version_checker package for semver regex

ExceptionFactory = t.Callable[[str, str, str], Exception]
ClientCallback = t.Callable[[str, str], t.Tuple]

MatchConverter = t.Callable[[t.Match], t.Tuple]
MatchData = t.Tuple[str, t.List[t.Any], t.Callable[[t.Match], t.Tuple]]
# 1st item (str): 'method'/'callable attribute' of the 're' python module)
# 2nd item (list): zero or more additional runtime arguments
# 3rd item (Callable): takes a Match object and return a tuple of strings

my_dir = os.path.dirname(os.path.realpath(__file__))

TOML = 'pyproject.toml'
TOML_FILE = os.path.abspath(os.path.join(my_dir, '..', TOML))

DEMO_SECTION: str = (
    "[tool.software-release]\nversion_variable = "
    "src/package_name/__init__.py:__version__"
)


def build_client_callback(data: MatchData, factory: ExceptionFactory) -> ClientCallback:

    def client_callback(file_path: str, regex: str) -> t.Tuple:
        with open(file_path, 'r') as _file:
            contents = _file.read()
        match = getattr(re, data[0])(regex, contents, *data[1])
        if match:
            extracted_tuple = data[2](match)
            return extracted_tuple
        else:
            raise factory(file_path, regex, contents)
    return client_callback


# PARSERS

software_release_parser = build_client_callback((
    'search',
    [re.MULTILINE,],
    lambda match: (match.group(1), match.group(2))
),
    lambda file_path, reg, string: RuntimeError(
                "Expected to find the '[tool.software-release]' section, in "
                f"the '{file_path}' file, with key "
                "'version_variable'.\nFor example:\n"
                f"{DEMO_SECTION}\n "
                "indicates that the version string should be looked up in "
                f"the src/package_name/__init__.py file and specifically "
                "a '__version__ = 1.2.3' kind of line is expected to be found."
            )
)


version_file_parser = build_client_callback((
    'search',
    [re.MULTILINE,],
    lambda match: (match.group(1),)
),
    lambda file_path, reg, string: AttributeError(
            "Could not find a match for regex {regex} when applied to:".format(
                regex=reg
            ) + "\n{content}".format(content=string)
        )
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
    version_specification = \
        r"version_variable[\ \t]*=[\ \t]*['\"]?([\w\.]+(?:/[\w\.]+)*):(\w+)['\"]?"
    regex = f"{header}{sep}{version_specification}"

    file_name_with_version, version_variable_name = \
        software_release_parser(software_release_cfg, regex)

    file_with_version_string = \
        os.path.abspath(os.path.join(my_dir, '../', file_name_with_version))

    if not os.path.isfile(file_with_version_string):
        raise FileNotFoundError(
            f"Path '{file_with_version_string} does not appear to be valid. "
            f"Please go to the '{software_release_cfg}' file, at the"
            " [tool.software-release] section and set the 'version_variable' "
            "key with a valid file path (to look for the version string). "
            f"For example:\n{DEMO_SECTION}\n"
        )

    reg = f'^{version_variable_name}' + r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'
    version, = version_file_parser(file_with_version_string, reg)
    return version


def _main():
    try:
        version_string = parse_version(TOML_FILE)
        print(version_string)
        return 0
    except (RuntimeError, FileNotFoundError, AttributeError) as exception:
        print(exception)
        return 1


def main():
    sys.exit(_main())


if __name__ == '__main__':
    main()
