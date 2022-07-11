from typing import MutableMapping

import attr

from .check_service import ServiceChecker


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Checkers:
    _checkers: MutableMapping

    def __getitem__(self, item):
        return self._checkers[item]

    def __iter__(self):
        return iter(self._checkers.values())

    @staticmethod
    def from_hosting_info(hosting_infos, activate_flag, config_file):
        return Checkers(
            {
                str(x.service): ServiceChecker.create(x, activate_flag, config_file)
                for x in hosting_infos
            }
        )
