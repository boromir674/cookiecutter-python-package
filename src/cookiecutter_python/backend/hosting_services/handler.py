from typing import Mapping

import attr

from .handle_hosting_service_check import CheckHostingServiceHandler


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Handlers:
    handlers: Mapping

    def __getattr__(self, service_name):
        return lambda request_result: self.handlers[service_name](request_result)

    def __call__(self, request_result):
        return getattr(self, request_result.service_name)(request_result)

    @staticmethod
    def from_checkers(checkers):
        return Handlers({str(x): CheckHostingServiceResultHandler(str(x)) for x in checkers})


@attr.s(auto_attribs=True, slots=True, frozen=True)
class CheckHostingServiceResultHandler:
    service_name: str

    @staticmethod
    def is_future_response_200(result) -> bool:
        return result.future.result().status_code == 200

    def __call__(self, request_result):
        if request_result:
            return CheckHostingServiceHandler(
                lambda x: self.is_future_response_200(request_result), self.service_name
            )(request_result.name)
