from typing import Callable

import attr

from .check_web_hosting_service import WebHostingServiceChecker
from .exceptions import ContextVariableDoesNotExist
from .extract_name import NameExtractor

ExtractNameAble = Callable[[str], str]


@attr.s(auto_attribs=True, slots=True, frozen=True)
class ServiceChecker:
    name_extractor: ExtractNameAble
    web_service_checker: WebHostingServiceChecker
    activate_flag: bool
    config_file_path: str

    def __call__(self):
        """Check the remote server for existing resource, if feture is enabled.

        Returns:
            Optional[CheckResult]: result of the check operation
        """
        if self.activate_flag:
            # TODO Improvement: enable feature regardless of default_config
            try:
                name = self.name_extractor(self.config_file_path)
                result = self.web_service_checker(name)
                return result
            except ContextVariableDoesNotExist as error:
                print(error)
        return None

    @property
    def service_name(self):
        return str(self.web_service_checker)

    def __str__(self):
        return str(self.web_service_checker)

    @staticmethod
    def create(hosting_service_info, activate_flag: bool, config_file_path):
        return ServiceChecker(
            NameExtractor.create(hosting_service_info),
            WebHostingServiceChecker.create(hosting_service_info.service),
            activate_flag,
            config_file_path,
        )
