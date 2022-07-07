import sys
from typing import Callable

from requests.exceptions import ConnectionError

__all__ = ['check_readthedocs_handler']


def _available_on_readthedocs(callback, project_slug: str):
    try:
        res: bool = callback(project_slug)
    except ConnectionError as error:
        print(error, file=sys.stderr)
        print("Could not establish connection to readthedocs.")
        print(
            "Could not determine whether the selected readthedocs project "
            f"'{project_slug}' is already taken."
        )
    except Exception as error:  # ie network failure
        print(str(error), file=sys.stdout)
    else:
        if res:
            print(
                f"Documentation Project with name '{project_slug}' already"
                " EXISTS on readthedocs.org!"
            )
            print(
                "You shall rename your Documentation Project slug"
                " before publishing to readthedocs!"
            )
        else:
            print("Name '{name}' IS available on readthedocs.org!".format(name=project_slug))
            print("You will be able to publish your Documentation on readthedocs as it is!")


def check_readthedocs_handler(callback: Callable[[str], bool]) -> Callable[[str], None]:
    def _handler(project_slug: str) -> None:
        _available_on_readthedocs(callback, project_slug)

    return _handler
