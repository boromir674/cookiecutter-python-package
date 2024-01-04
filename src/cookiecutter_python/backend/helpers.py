import logging
import typing as t

from .load_config import get_interpreters_from_yaml, load_yaml

GivenInterpreters = t.Mapping[str, t.Sequence[str]]

logger = logging.getLogger(__name__)


def parse_context(config_file: str):
    data = load_yaml(config_file)
    user_context = data['default_context']
    from cookiecutter_python.handle.interactive_cli_pipeline import InteractiveDialogsPipeline
    pipe = InteractiveDialogsPipeline()
    import json
    c = json.loads(user_context.get('interpreters', '{}'))
    cc = c.get('supported-interpreters', [
            "3.6",
            "3.7",
            "3.8",
            "3.9",
            "3.10",
            "3.11"
        ])

    res = pipe.process([
        ["module", "module+cli", "pytest-plugin"],
        user_context.get('full_name', None),
        cc,
        # Project NAME
        user_context.get('project_name', None),  
    ])
    return res
