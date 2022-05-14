import sys

from requests.exceptions import ConnectionError

from .check_pypi import is_registered_on_pypi

__all__ = ['available_on_pypi']


def available_on_pypi(package_name: str):
    try:
        res: bool = is_registered_on_pypi(package_name)
    except ImportError as error:
        print(error)
        print(
            "If you want to enable the 'check_pypi' feature, "
            "Please also install the [check_pypi] requirements (see setup.cfg)"
        )
    except ConnectionError as error:
        print(error, file=sys.stderr)
        print("Could not establish connection to pypi.")
        print(
            f"Could not determine whether the selected pypi name '{package_name}' is already taken."
        )

    except Exception as error:  # ie network failure
        print(str(error), file=sys.stderr)
    else:
        if res:
            print(
                "Package with name '{name}' already EXISTS on pypi.org!".format(
                    name=package_name
                )
            )
            print("You shall rename your Python Package before publishing to pypi!")
        else:
            print("Name '{name}' IS available on pypi.org!".format(name=package_name))
            print("You will be able to publish your Python Package on pypi as it is!")
