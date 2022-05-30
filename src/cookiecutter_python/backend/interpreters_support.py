import typing as t

InterpretersSequence = t.Sequence[str]


# TODO Improvement: use an Enum
# SUPPORTED = {
#     'py35',
#     'py36',
#     'py37',
#     'py38',
#     'py39',
#     'py310',
#     'py311',
# }

SUPPORTED = {
    '3.5',
    '3.6',
    '3.7',
    '3.8',
    '3.9',
    '3.10',
    '3.11',
}


def verify_input_interpreters(interpreters: InterpretersSequence) -> None:
    user_interpreters_set = set(interpreters)
    if len(user_interpreters_set) != len(interpreters):
        raise InvalidInterpretersError("Found duplicate interpreters!")

    if not user_interpreters_set.issubset(SUPPORTED):
        # not all user requested interpreters are included in the supported ones
        raise InvalidInterpretersError(
            "Unsupported interpreter given Error!\n"
            + "Given interpreters: [{given}]\n".format(given=', '.join(interpreters))
            + "Supported interpreters: [{supported}]\n".format(supported=', '.join(SUPPORTED))
            + "Unsupported interpreters: [{unsupported}]".format(
                unsupported=', '.join(iter(unsupported_interpreters(interpreters)))
            )
        )


def unsupported_interpreters(interpreters: InterpretersSequence) -> t.Iterator[str]:
    for interpreter in interpreters:
        if interpreter not in SUPPORTED:
            yield interpreter


class InvalidInterpretersError(Exception):
    pass
