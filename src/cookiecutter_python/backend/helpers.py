"""Interactive Dialog wizards to gather User Input for Context variables."""

import json
import logging
import typing as t
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from cookiecutter_python.handle.interactive_cli_pipeline import (
    InteractiveDialogsPipeline,
)


logger = logging.getLogger(__name__)

my_dir = Path(__file__).parent.absolute()


GivenInterpreters = t.Mapping[str, t.Sequence[str]]


def parse_context(config_file: str):
    """Render Context on demand, using cookiecutter.json and optional config file."""

    # use whatever way cookiecutter uses to render the cookiecutter.json
    # cookiecutter uses Jinja2 to render files
    env = Environment(
        loader=FileSystemLoader(str(my_dir / '..')),
        extensions=['jinja2_time.TimeExtension'],  # shipped with cookiecutter 1.7
        # Issue: [B701:jinja2_autoescape_false] By default, jinja2 sets autoescape to False. Consider using autoescape=True or use the select_autoescape function to mitigate XSS vulnerabilities.
        # Severity: High   Confidence: High
        # CWE: CWE-94 (https://cwe.mitre.org/data/definitions/94.html)
        # More Info: https://bandit.readthedocs.io/en/1.7.7/plugins/b701_jinja2_autoescape_false.html
        autoescape=True,
    )

    template = env.get_template('cookiecutter.json')
    rendered = template.render({'cookiecutter': {}})

    assert isinstance(rendered, str)

    cook_json: t.Mapping[str, t.Any] = json.loads(rendered)

    # in cookiecutter 1.7, a 'choice' variable is a json array
    choices = {k: v for k, v in cook_json.items() if isinstance(v, list)}

    if config_file:
        from .user_config_proxy import get_user_config

        data = get_user_config(config_file, default_config=False)
        # data = load_yaml(config_file)
        user_default_context = data['default_context']
        _interpreters: t.Mapping[str, t.List[str]] = user_default_context.get(
            'interpreters', '{}'
        )
        if isinstance(_interpreters, str):
            logger.warning(
                "Interpreters expected to be loaded in a python dict already. Got a string instead."
            )
            logger.info("Converting interpreters %s to a python dict", _interpreters)
            _interpreters = json.loads(_interpreters)
        user_interpreters = _interpreters
    else:
        user_default_context = {}
        user_interpreters = cook_json['interpreters']

    context_defaults = dict(
        cook_json,
        **{k: v for k, v in user_default_context.items()},
        **{k: v[0] for k, v in choices.items() if k not in user_default_context},
    )

    # Render cookiecutter.json again with context to resolve derived fields
    # This ensures derived fields like pkg_name get computed properly
    template = env.get_template('cookiecutter.json')
    rendered_with_context = template.render({'cookiecutter': context_defaults})
    resolved_cook_json: t.Mapping[str, t.Any] = json.loads(rendered_with_context)

    # Update context_defaults with resolved derived fields, but preserve user config values
    for key, value in resolved_cook_json.items():
        # Only update if the key wasn't explicitly provided by user
        if key not in user_default_context:
            context_defaults[key] = value

    pipe = InteractiveDialogsPipeline()

    # Build the context dynamically to include all fields
    interactive_context = {}

    # Simple fields (no choices)
    simple_fields = [
        'project_name',
        'project_slug',
        'pkg_name',
        'repo_name',
        'readthedocs_project_slug',
        'docker_image',
        'full_name',
        'author',
        'author_email',
        'github_username',
        'project_short_description',
        'pypi_subtitle',
        'version',
    ]

    for field in simple_fields:
        if field in context_defaults:
            interactive_context[field] = context_defaults[field]

    # Choice fields (with options)
    choice_fields = [
        'project_type',
        'initialize_git_repo',
        'docs_builder',
        'rtd_python_version',
        'cicd',
        # Include Grafana, Loki stack no/yes
        'include_observability',  # ["no", "yes"]
    ]

    for field in choice_fields:
        if field in choices:
            interactive_context[field] = {
                'default': context_defaults[field],
                'choices': choices[field],
            }

    # Special handling for interpreters
    interactive_context["supported-interpreters"] = {
        'choices': [
            (choice, True)
            for choice in user_interpreters.get(
                'supported-interpreters',
                ["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"],
            )
        ],
    }

    # assert choices['rtd_python_version'] == [], f"DEBUG: {choices['rtd_python_version']}"
    res = pipe.process([interactive_context])
    return res
