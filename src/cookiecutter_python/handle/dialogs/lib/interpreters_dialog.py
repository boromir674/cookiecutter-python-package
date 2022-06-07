import typing as t

try:
    from PyInquirer import prompt
except ImportError:

    def prompt(*args, **kwargs):
        return {}


from ..dialog import InteractiveDialog


@InteractiveDialog.register_as_subclass('interpreters-checkbox')
class InterpretersCheckbox(InteractiveDialog):
    def dialog(self, *args, **kwargs):
        return self._dialog(*args, **kwargs)

    def _dialog(
        self, choices: t.Dict[str, t.Union[str, bool]]
    ) -> t.Dict[str, t.Sequence[str]]:

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
