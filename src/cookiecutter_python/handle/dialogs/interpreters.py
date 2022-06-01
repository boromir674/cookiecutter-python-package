import typing as t

from PyInquirer import prompt


def dialog(choices: t.Dict[str, t.Union[str, bool]]) -> t.Dict[str, t.Sequence[str]]:

    return prompt(
        [
            # Question 1
            {
                'type': 'checkbox',
                'name': 'supported-interpreters',
                'message': 'Select the python Interpreters you wish to support',
                'choices': choices,
            },
        ]
    )
