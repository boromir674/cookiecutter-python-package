from typing import Mapping, Union, Sequence, Callable, Optional, Any

PyInquirerQuestion = Mapping[str, Optional[Union[str, Mapping, Callable]]]

PyInquirerPromtQuestions = Union[PyInquirerQuestion, Sequence[PyInquirerQuestion]]

PyInquirerAnswers = Mapping[str, Any]


def prompt(
    questions: PyInquirerPromtQuestions,
    answers: Optional[PyInquirerAnswers] = None,
    **kwargs: Any
) -> PyInquirerAnswers: ...
