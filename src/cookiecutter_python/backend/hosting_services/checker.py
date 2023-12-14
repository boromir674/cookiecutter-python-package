from typing import Union

import attr

from .checkers import Checkers


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Checker:
    config_file: Union[None, str]
    default_config: Union[None, bool]
    checkers: Checkers

    def __getattr__(self, service_name: str):
        return self.checkers[service_name]

    def __iter__(self):
        return iter(self.checkers)

    @staticmethod
    def from_hosting_info(config_file, default_config, hosting_infos):
        """Activate Web Host Checks if user config and NOT default config"""
        return Checker(
            config_file,
            default_config,
            Checkers.from_hosting_info(
                hosting_infos,
                config_file and not default_config,
                config_file,
            ),
        )
