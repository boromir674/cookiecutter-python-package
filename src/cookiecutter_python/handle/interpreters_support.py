import typing as t

from PyInquirer import prompt


INTERPRETERS_ATTR = 'interpreters'


choices = [
    {
        'name': 'py35',
        'checked': False
    },
    {
        'name': 'py36',
        'checked': True
    },
    {
        'name': 'py37',
        'checked': True
    },
    {
        'name': 'py38',
        'checked': True
    },
    {
        'name': 'py39',
        'checked': True
    },
    {
        'name': 'py310',
        'checked': True
    },
    {
        'name': 'py311',
        'checked': False
    },
]

class WithUserInterpreters(t.Protocol):
    interpreters: t.Optional[t.Sequence[str]]


def handle(
    request: t.Optional[WithUserInterpreters] = None,
    no_input: bool =False,
) -> t.Sequence[str]:
    if request and hasattr(request, INTERPRETERS_ATTR):
        return getattr(request, INTERPRETERS_ATTR)
    if no_input:
        interpreters = {'supported-interpreters': [
            x['name'] for x in choices if x['checked']
        ]}
    else:
        interpreters =  dialog()

    interpreter_aliases = []
    for name in interpreters['supported-interpreters']:
        b = name.replace('py', '')
        interpreter_aliases.append(b[0] + '.' + b[1:]) 
    return {'supported-interpreters': interpreter_aliases}


def dialog() -> t.Sequence[str]:

    return prompt([
        # Question 1
        {
            'type': 'checkbox',
            'name': 'supported-interpreters',
            'message': 'Select the python Interpreters you wish to support',
        },

    ])
