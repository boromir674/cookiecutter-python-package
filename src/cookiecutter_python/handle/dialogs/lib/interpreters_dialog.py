from typing import Any, Callable, Mapping, Optional, Sequence, Union

from questionary import prompt

from ..dialog import InteractiveDialog

QuestionaryQuestion = Mapping[str, Optional[Union[str, Mapping, Callable]]]
QuestionaryPromtQuestions = Union[QuestionaryQuestion, Sequence[QuestionaryQuestion]]

QuestionaryAnswers = Mapping[str, Any]

# try:
#     from PyInquirer import prompt
# except ImportError:

#     def prompt(
#         questions: PyInquirerPromtQuestions, answers: PyInquirerAnswers = None, **kwargs: Any
#     ) -> PyInquirerAnswers:
#         return {}


@InteractiveDialog.register_as_subclass('interpreters-checkbox')
class InterpretersCheckbox(InteractiveDialog):
    def dialog(self, *args, **kwargs):
        return self._dialog(*args, **kwargs)

    @staticmethod
    def _dialog(choices: Mapping[str, Union[str, bool]]) -> Mapping[str, Sequence[str]]:

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
