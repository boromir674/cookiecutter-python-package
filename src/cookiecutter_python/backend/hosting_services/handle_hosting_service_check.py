import sys
import typing as t

import attr
from requests.exceptions import ConnectionError as RequestsConnectionError


HostingServiceChecker = t.Callable[[str], bool]


@attr.s(auto_attribs=True, slots=True)
class CheckHostingServiceHandler:
    check_hosting_service: HostingServiceChecker
    service_name: str = attr.ib(
        default=attr.Factory(lambda self: str(self.check_hosting_service), takes_self=True)
    )
    package_name: str = attr.ib(init=False, default=None)

    def _handle_connection_error(self, error):
        print(error, file=sys.stderr)
        print(
            f"Could not establish connection to {self.service_name}.\n"
            "Could not determine whether the name "
            f"'{self.package_name}' is already \"taken\" on {self.service_name}."
        )

    def __call__(self, package_name: str):
        try:
            res: bool = self.check_hosting_service(package_name)
        except RequestsConnectionError as error:
            self.package_name = package_name  # a package "slug" (name)
            self._handle_connection_error(error)
        except Exception as error:  # any other error
            print(str(error), file=sys.stdout)
        else:
            if res:
                print(
                    f"Project registered under '{package_name}' is already TAKEN on "
                    f"{self.service_name}.\nYou shall rename your Python Package first, if you"
                    f" choose to publish it on {self.service_name}!"
                )
            else:
                print(
                    f"Name '{package_name}' is AVAILABLE on {self.service_name}!\n"
                    "You will not need to rename your Python Package if you choose to publish"
                    f" it on {self.service_name} :)"
                )
