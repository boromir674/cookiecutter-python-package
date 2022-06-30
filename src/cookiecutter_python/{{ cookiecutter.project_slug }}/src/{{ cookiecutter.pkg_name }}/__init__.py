__version__ = '{{ cookiecutter.version }}'
{% if cookiecutter.project_type == "pytest-plugin" %}
from .fixtures import my_fixture

__all__ = ['my_fixture']
{% endif %}