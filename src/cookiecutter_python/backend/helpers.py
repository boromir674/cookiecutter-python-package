import json
import logging
import typing as t


GivenInterpreters = t.Mapping[str, t.Sequence[str]]

logger = logging.getLogger(__name__)


def parse_context(config_file: str):
    """Render Context on demand, using cookiecutter.json and optional config file."""
    from pathlib import Path

    my_dir = Path(__file__).parent.absolute()

    # use whatever way cookiecutter uses to render the cookiecutter.json
    # cookie uses Jinja2

    from jinja2 import Environment, FileSystemLoader

    # render file
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

    from cookiecutter_python.handle.interactive_cli_pipeline import (
        InteractiveDialogsPipeline,
    )

    pipe = InteractiveDialogsPipeline()

    # assert choices['rtd_python_version'] == [], f"DEBUG: {choices['rtd_python_version']}"
    res = pipe.process(
        [
            {
                "project_name": context_defaults['project_name'],
                "project_type": {
                    'default': context_defaults['project_type'],
                    'choices': choices['project_type'],
                },
                "full_name": context_defaults['full_name'],
                "author_email": context_defaults['author_email'],
                "github_username": context_defaults['github_username'],
                "project_short_description": context_defaults['project_short_description'],
                # "release_date": context_defaults['release_date'],
                # "year": context_defaults['year'],
                "version": context_defaults['version'],
                "initialize_git_repo": {
                    'default': context_defaults['initialize_git_repo'],
                    'choices': choices['initialize_git_repo'],
                },
                "supported-interpreters": {
                    # 'default': context_defaults['initialize_git_repo'],
                    'choices': [
                        (choice, True)
                        for choice in user_interpreters.get(
                            'supported-interpreters',
                            ["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"],
                        )
                    ],
                },
                "docs_builder": {
                    'default': context_defaults['docs_builder'],
                    'choices': choices['docs_builder'],
                },
                "rtd_python_version": {
                    'default': context_defaults['rtd_python_version'],
                    'choices': choices['rtd_python_version'],
                },
                "cicd": {
                    'default': context_defaults['cicd'],
                    'choices': choices['cicd'],
                },
            }
        ]
    )
    return res
