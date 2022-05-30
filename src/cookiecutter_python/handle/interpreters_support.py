import typing as t

INTERPRETERS_ATTR = 'interpreters'

from .dialogs.interpreters import dialog

choices = [
    {'name': 'py35', 'checked': False},
    {'name': 'py36', 'checked': True},
    {'name': 'py37', 'checked': True},
    {'name': 'py38', 'checked': True},
    {'name': 'py39', 'checked': True},
    {'name': 'py310', 'checked': True},
    {'name': 'py311', 'checked': False},
]


def handle() -> t.Sequence[str]:
    """Hande request to create the 'supported interpreters' used in the Project generationfor the generate a project with supporting python interpreters.

    Args:
        request (t.Optional[WithUserInterpreters], optional): [description]. Defaults to None.
        no_input (bool, optional): [description]. Defaults to False.

    Returns:
        t.Sequence[str]: [description]
    """
    return {
        'supported-interpreters': transform_interpreters(
            dialog(choices)['supported-interpreters']
        )
    }


def transform_interpreters(interpreters: t.Sequence[str]) -> t.Sequence[str]:
    interpreter_aliases = []
    for name in interpreters:
        b = name.replace('py', '')
        interpreter_aliases.append(b[0] + '.' + b[1:])
    print('ALIASES:', interpreter_aliases)
    return interpreter_aliases

