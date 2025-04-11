import typing as t

from .input_sanitization import Sanitize


InterpretersSequence = t.Sequence[str]


# TODO Improvement: use an Enum

# Must be maintained to match the available python interpreters on the CI Provider
VALID_PYTHON_VERSIONS = {
    '3.6',
    '3.7',
    # TODO: verify which versions are available on the CI Provider and eliminate
    #  the ones that are not available
    # TODO: from remaining available on CI versions, start throwing warning to user if theyt are about to be elminated
    # from CI in the near future, or if they are an old unmaintained python version
    '3.8',
    '3.9',
    '3.10',
    '3.11',
    '3.12',
    '3.13',
    '3.14',
}


@Sanitize.register_sanitizer('interpreters')
def verify_input_interpreters(interpreters: InterpretersSequence) -> None:
    user_interpreters_set = set(interpreters)
    if len(user_interpreters_set) != len(interpreters):
        raise InvalidInterpretersError("Found duplicate interpreters!")

    if not user_interpreters_set.issubset(VALID_PYTHON_VERSIONS):
        # not all user requested interpreters are included in the supported ones
        raise InvalidInterpretersError(
            "Unsupported interpreter given Error!\n"
            + "Given interpreters: [{given}]\n".format(given=', '.join(interpreters))
            + "Supported interpreters: [{supported}]\n".format(
                supported=', '.join(VALID_PYTHON_VERSIONS)
            )
            + "Unsupported interpreters: [{unsupported}]".format(
                unsupported=', '.join(iter(unsupported_interpreters(interpreters)))
            )
        )


def unsupported_interpreters(interpreters: InterpretersSequence) -> t.Iterator[str]:
    for interpreter in interpreters:
        if interpreter not in VALID_PYTHON_VERSIONS:
            yield interpreter


@Sanitize.register_exception('interpreters')
class InvalidInterpretersError(Exception):
    pass
