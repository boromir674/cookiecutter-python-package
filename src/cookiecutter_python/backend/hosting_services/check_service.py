import logging
from typing import Callable

import attr

from .check_web_hosting_service import WebHostingServiceChecker
from .exceptions import ContextVariableDoesNotExist
from .extract_name import NameExtractor


logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class ServiceChecker:
    # parser of User Config (YAML) file
    name_extractor: Callable[[str], str]  # (config_file: str) -> str

    # Resolves URLs and makes Future HTTP Requests
    web_service_checker: WebHostingServiceChecker

    # Hard switch to enable/disable feature
    activate_flag: bool

    # Path to User Config (YAML) file, to parse at runtime, on __call__ invoke
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
                # we assume that client deliberately had the activate flag on
                # only because they know that the way the Generator has been
                # parametrized (ie from CLI),
                # accounting for User Config or Default Config precedance, is such
                # that on Generator call the User Config will have precendence.
                # But this is design to be call in pre_main, so rendering has
                # not happened yet, so we can't rely on the User Config.

                # We could manullay render the cookiecutter.json file, with jinja2

                # or we can signal, that this can be called after rendering
                # in post_main, but we are going to loose fancy Futures HTTP!
                # and we are going to have to do the HTTP request in the main thread
                # and we are going to have to do it in a blocking way, but still at the very end

                # Atm, leaning more towards an INFO than a WARNING
                logger.info(
                    "Skipping check of remote server, because of missing context variable"
                )
                logger.info(error)
                # atm service checker can only rely on user config yaml file
                # the info can be derived from static cookiecutter.json file
                # or after rendering the template
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
