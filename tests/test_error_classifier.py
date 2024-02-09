import typing as t

import pytest


@pytest.fixture
def exception_classifier() -> t.Callable[[Exception], t.Optional[str]]:
    from cookiecutter_python.exceptions import error_2_str

    return error_2_str


@pytest.mark.parametrize(
    'unknown_exception',
    [
        TypeError,
        ValueError,
    ],
)
def test_unknown_exceptions_are_classified_as_None(
    # GIVEN some Exceptions that are Unknown to the Classifier
    unknown_exception: Exception,
    # GIVEN an Exceptions Classifier
    exception_classifier: t.Callable[[Exception], t.Optional[str]],
):
    # WHEN the Exceptions are classified
    result = exception_classifier(unknown_exception)

    # THEN the Exceptions are classified as None
    assert result is None


# this tests captures the logs to print them and help debugging
def test_exceptions_that_hinder_generator_are_classified_as_critical(
    # GIVEN an Exceptions Classifier
    exception_classifier: t.Callable[[Exception], t.Optional[str]],
):
    # GIVEN some Exceptions that hinder the Generator
    from cookiecutter.exceptions import (
        ContextDecodingException,
        NonTemplatedInputDirException,
    )

    critical_exceptions = [
        NonTemplatedInputDirException(),
        ContextDecodingException(),
    ]
    # SANITY
    from cookiecutter_python.exceptions import cookiecutter_exceptions

    assert len(cookiecutter_exceptions) > 0, "cookiecutter_exceptions is empty"

    # WHEN the Exceptions are classified
    result = [exception_classifier(exception) for exception in critical_exceptions]

    # THEN the Exceptions are classified as Critical
    assert all([x == 'critical' for x in result])


def test_exceptions_not_hindering_generator_are_classified_as_non_critical(
    # GIVEN an Exceptions Classifier
    exception_classifier: t.Callable[[Exception], t.Optional[str]],
):
    # GIVEN some Exceptions that do not hinder the Generator
    from cookiecutter.exceptions import UndefinedVariableInTemplate
    from jinja2.exceptions import UndefinedError

    non_critical_exceptions = [
        UndefinedVariableInTemplate('', UndefinedError(), {}),
    ]

    # WHEN the Exceptions are classified
    result = [exception_classifier(exception) for exception in non_critical_exceptions]

    # THEN the Exceptions are classified as Non-Critical
    assert all([x == 'non-critical' for x in result])
