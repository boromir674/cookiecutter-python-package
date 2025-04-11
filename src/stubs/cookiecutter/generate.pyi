# # Prod function
# def generate_context(
#     context_file='cookiecutter.json', default_context=None, extra_context=None
# ):

from typing import Any, Mapping, Optional

def generate_context(
    context_file: str = 'cookiecutter.json',
    default_context: Optional[Mapping[str, Any]] = None,
    extra_context: Optional[Mapping[str, Any]] = None,
) -> Mapping[str, Any]: ...
