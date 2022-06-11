import re
import typing as t

from ..input_sanitization import Sanitize
from .sanitize_reg_input import RegExSanitizer


class VersionSanitizer(RegExSanitizer):
    regex = re.compile(
        r'^(?P<major>0|[1-9]\d*)'
        r'\.'
        r'(?P<minor>0|[1-9]\d*)'
        r'\.'
        r'(?P<patch>0|[1-9]\d*)'
        r'(?:-'
        r'(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+'
        r'(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    )
    exception_msg = 'Expected a Semantic Version value'

    @classmethod
    def log_message(cls, error, string) -> t.Tuple[t.Union[str, t.Mapping], ...]:
        return (
            "%s: %s",
            str(error),
            {
                'semver_regex': str(cls.regex.pattern),
                'version_string': str(string),
            },
        )


version_sanitizer = VersionSanitizer()


@Sanitize.register_sanitizer('semantic-version')
def sanitize_version(version: str) -> None:
    version_sanitizer(version)
