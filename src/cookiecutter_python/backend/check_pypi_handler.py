import sys
from .check_pypi import is_registered_on_pypi

__all__ = ['handle_availability', 'available_on_pypi']

def handle_availability(registered_on_pypi: bool, package_name: str) -> None:
    if registered_on_pypi:
        print(
            "Package with name '{name}' already EXISTS on pypi.org!".format(
                name=package_name
            )
        )
        print("You shall rename your Python Package before publishing to pypi!")
    else:
        print(
            "Name '{name}' IS available on pypi.org!".format(name=package_name)
        )
        print("You will be able to publish your Python Package on pypi as it is!")


def available_on_pypi(package_name: str):
    try:
        res: bool = is_registered_on_pypi(package_name)
    except ImportError as error:
        print(error)
        print("If you want to enable the 'check_pypi' feature, "
        "Please install along with the [check_pypi] requirements (see setup.cfg)")
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
            print(
                "Name '{name}' IS available on pypi.org!".format(name=package_name)
            )
            print("You will be able to publish your Python Package on pypi as it is!")

