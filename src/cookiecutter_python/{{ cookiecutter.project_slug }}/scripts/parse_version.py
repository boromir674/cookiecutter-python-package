#!/usr/bin/env python


import os
import re
import sys

my_dir = os.path.dirname(os.path.realpath(__file__))

SETUP_CFG_FILENAME = 'setup.cfg'
SETUP_CFG = os.path.join(my_dir, '../', SETUP_CFG_FILENAME)


def main():
    """Get the package version string provided that the developer has setup indication how to find it. Reads the
    [semantic_release] section found in setup.cfg and then determines where is the actual version string
    """
    # Automatically compute package version from the [semantic_release] section in setup.cfg
    with open(SETUP_CFG, 'r') as _file:
        regex = r"\[semantic_release\][\w\s=/\.:\d]+version_variable[\ \t]*=[\ \t]*([\w\.]+(?:/[\w\.]+)*):(\w+)"
        match = re.search(regex, _file.read(), re.MULTILINE)
        if match:
            file_with_version_string = os.path.join(my_dir, '../', match.group(1))
            variable_holding_version_value = match.group(2)
        else:
            raise RuntimeError(
                f"Expected to find the '[semantic_release]' section, in the '{SETUP_CFG}' file, with key "
                f"'version_variable'.\nFor example:\n[semantic_release]\nversion_variable = "
                f"src/package_name/__init__.py:__version__\n indicated that the version string should be looked up in "
                f"the src/package_name/__init__.py file registered under the __version__ 'name'"
            )

    # (it does not have to be a.py file)
    # to indicate that the version is stored in the '__version__'
    if not os.path.isfile(file_with_version_string):
        raise FileNotFoundError(
            f"Path '{file_with_version_string} does not appear to be valid. Please go to the '{SETUP_CFG}' file, at the"
            f" [semantic_release] section and set the 'version_variable' key with a valid file path (to look for the "
            f"version string)"
        )

    reg_string = r'\s*=\s*[\'\"]([^\'\"]*)[\'\"]'

    with open(file_with_version_string, 'r') as _file:
        content = _file.read()
        reg = f'^{variable_holding_version_value}' + reg_string
        match = re.search(reg, content, re.MULTILINE)
        if match:
            _version = match.group(1)
            return _version
        raise AttributeError(
            f"Could not find a match for regex {reg} when applied to:\n{content}"
        )


if __name__ == '__main__':
    try:
        version_string = main()
        print(version_string)
    except (RuntimeError, FileNotFoundError, AttributeError) as exception:
        print(exception)
        sys.exit(1)
