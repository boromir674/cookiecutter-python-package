from typing import Mapping

import attr


class ValueExtractor:
    def __call__(self, data: Mapping) -> str:
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


@attr.s(auto_attribs=True, slots=True, frozen=True)
class BaseValueExtractor(ValueExtractor):
    key_name: str

    def __call__(self, data: Mapping) -> str:
        return data[self.key_name]

    def __str__(self):
        return self.key_name
