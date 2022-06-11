import re
import typing as t

from ..input_sanitization import Sanitize
from .sanitize_reg_input import RegExSanitizer


class ModuleNameSanitizer(RegExSanitizer):
    regex = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]+$')
    exception_msg = 'Expected a valid Python Module name value'

    @classmethod
    def log_message(cls, error, module) -> t.Tuple[t.Union[str, t.Mapping], ...]:
        return (
            "%s: %s",
            str(error),
            {
                'module_name_regex': str(cls.regex.pattern),
                'module_name': str(module),
            },
        )


module_name_sanitizer = ModuleNameSanitizer()


@Sanitize.register_sanitizer('module-name')
def sanitize_module_name(module_name: str) -> None:
    module_name_sanitizer(module_name)
