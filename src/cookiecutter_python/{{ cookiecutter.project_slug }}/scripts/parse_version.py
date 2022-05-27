#!/usr/bin/env python

import os
import re
import sys

my_dir = os.path.dirname(os.path.realpath(__file__))

SOFTWARE_RELEASE_CFG_FILE = 'pyproject.toml'
SOFTWARE_RELEASE_CFG = os.path.abspath(
    os.path.join(os.path.dirname(my_dir), SOFTWARE_RELEASE_CFG_FILE)
)


def parse_version(software_release_cfg: str):
    """Get the package version string prpyproject.tomlovided that the developer has setup indication how to find it. Reads the
    [too.lsoftware-release] section found in setup.cfg and then determines where is the actual version string
    """
    # Automatically compute package version from the [software-release] section in setup.cfg
    with open(software_release_cfg, 'r') as _file:
        regex = r"\[tool\.software-release\][\w\s=/\.:\d]+version_variable[\ \t]*=[\ \t]*['\"]?([\w\.]+(?:/[\w\.]+)*):(\w+)['\"]?"
        match = re.search(regex, _file.read(), re.MULTILINE)
        if match:
            file_with_version_string = os.path.join(my_dir, '../', match.group(1))
            variable_holding_version_value = match.group(2)
        else:
            raise RuntimeError(
                f"Expected to find the '[software-release]' section, in the '{software_release_cfg}' file, with key "
                f"'version_variable'.\nFor example:\n[tool.software-release]\nversion_variable = "
                f"src/package_name/__init__.py:__version__\n indicated that the version string should be looked up in "
                f"the src/package_name/__init__.py file registered under the __version__ 'name'"
            )

    # (it does not have to be a.py file)
    # to indicate that the version is stored in the '__version__'
    if not os.path.isfile(file_with_version_string):
        raise FileNotFoundError(
            f"Path '{file_with_version_string} does not appear to be valid. Please go to the '{software_release_cfg}' file, at the"
            " [tool.software-release] section and set the 'version_variable' key with a valid file path (to look for the "
            "version string). For example:\n[tool.software-release]\nversion_variable = "
            "src/package_name/__init__.py:__version__\n"
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


def _main():
    try:
        version_string = parse_version(SOFTWARE_RELEASE_CFG)
        print(version_string)
        return 0
    except (RuntimeError, FileNotFoundError, AttributeError) as exception:
        print(exception)
        return 1


def main():
    sys.exit(_main())


if __name__ == '__main__':
    main()
