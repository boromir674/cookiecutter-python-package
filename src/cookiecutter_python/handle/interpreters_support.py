import typing as t

from .dialogs import InteractiveDialog

INTERPRETERS_ATTR = 'interpreters'


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
    """Get the 'supported interpreters' data, from user's input in interactive dialog.

    Args:
        request (t.Optional[WithUserInterpreters], optional): [description]. Defaults to None.
        no_input (bool, optional): [description]. Defaults to False.

    Returns:
        t.Sequence[str]: [description]
    """
    return InteractiveDialog.create('interpreters-checkbox')(
        [{'name': version, 'checked': True} for version in choices] if choices else CHOICES
    )
