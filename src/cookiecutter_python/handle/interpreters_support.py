import typing as t

INTERPRETERS_ATTR = 'interpreters'

from .dialogs.interpreters import dialog

CHOICES = [  # this should match the cookiecutter.json
    # TODO Improvement: dynamically read from cookiecutter.json
    {'name': '3.6', 'checked': True},
    {'name': '3.7', 'checked': True},
    {'name': '3.8', 'checked': True},
    {'name': '3.9', 'checked': True},
    {'name': '3.10', 'checked': True},
    {'name': '3.11', 'checked': False},
    {'name': '3.12', 'checked': False},
]


def handle(choices: t.Optional[t.Sequence[str]] = None) -> t.Dict[str, t.Sequence[str]]:
    """Hande request to create the 'supported interpreters' used in the Project generationfor the generate a project with supporting python interpreters.

    Args:
        request (t.Optional[WithUserInterpreters], optional): [description]. Defaults to None.
        no_input (bool, optional): [description]. Defaults to False.

    Returns:
        t.Sequence[str]: [description]
    """
    return dialog(
        [{'name': version, 'checked': True} for version in choices] if choices else CHOICES
    )
    # return {'supported-interpreters': dialog(
    #     [{'name': version, 'checked': True} for version in choices] if choices else CHOICES)['supported-interpreters']}
