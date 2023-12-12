"""Internal configuration for Documentation Generation."""

import typing as t
from pathlib import Path

# Runtime folder path of {{ cookiecutter.project_slug }}
PROJ_TEMPLATE_DIR: Path = Path(__file__).parent.parent / '{{ cookiecutter.project_slug }}'

# Reminder: the Template Design (TD) is defined by the:
#   - Template Variables; ie cookiecutter.json
#   - Project Template (root dir); ie /usr/lib/python/site-packages/cookiecutter_python/{{ cookiecutter.project_slug }}


def get_docs_gen_internal_config() -> t.Dict[str, str]:
    """Derive the internal configuration for Documentation Generation.

    Information included:
        - the folder where we each docs builder will generate the docs.
          We locate the template folder for each docs builder, which is the
          Single Source of Truth for the docs builder's output folder.
    """
    # find folders in PROJ_TEMPLATE_DIR with "docs-*"" glob pattern
    # and return a mapping of doc builder ID to their docs template folder
    # ie: {'mkdocs': 'docs-mkdocs', 'sphinx': 'docs-sphinx'}
    doc_builder_id_2_doc_folder: t.Dict[str, str] = {
        path.name.split('-')[1]: path.name
        for path in PROJ_TEMPLATE_DIR.glob('docs-*')
        if path.is_dir()
    }
    assert (
        doc_builder_id_2_doc_folder
    ), f"templated_proj_folder: {PROJ_TEMPLATE_DIR}, with files: {list(PROJ_TEMPLATE_DIR.glob('*'))}"
    # return the internal configuration (atm it's just the mapping above)
    return doc_builder_id_2_doc_folder
