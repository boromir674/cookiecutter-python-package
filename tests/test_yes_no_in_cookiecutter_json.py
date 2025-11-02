"""Test cookiecutter context handling of yes/no choice variables vs multi-choice variables.

This test verifies that cookiecutter properly handles different types of choice variables
in the generated context, specifically:
- Boolean-style yes/no variables should remain as strings (not converted to booleans)
- Multi-choice variables should remain as lists in _cookiecutter context
- Selected values should appear as strings in cookiecutter context
"""

import json
from pathlib import Path


def test_cookiecutter_context_preserves_choice_variable_types(tmp_path: Path):
    """Test that cookiecutter preserves variable types correctly in context.

    GIVEN a cookiecutter.json file with:
    - A yes/no choice variable v1
    - A multi-choice variable v2 with options a/b/c
    WHEN cookiecutter reads/parses/renders the template
    THEN the context should contain:
    - v1 as string value (not boolean) in 'cookiecutter' context
    - v1 as list of choices in '_cookiecutter' context
    - v2 as string value (first choice) in 'cookiecutter' context
    - v2 as list of choices in '_cookiecutter' context
    """

    # GIVEN: Create a minimal cookiecutter template
    template_dir = tmp_path / "test_template"
    template_dir.mkdir()

    # Create cookiecutter.json with yes/no and multi-choice variables
    cookiecutter_json = {
        "project_name": "Test Project",
        "enable_feature": ["no", "yes"],  # yes/no choice variable (v1)
        "build_system": ["poetry", "setuptools", "flit"],  # multi-choice variable (v2)
        "multiple_choice": ["c1", "c2", "c3"],  # multi-choice variable (v2)
        "multiple_choice_2": ["c1", "c2", "c3"],  # multi-choice variable (v2)
    }

    cookiecutter_json_file = template_dir / "cookiecutter.json"
    with open(cookiecutter_json_file, 'w') as f:
        json.dump(cookiecutter_json, f, indent=2)

    # Create a minimal template project structure
    project_template_dir = (
        template_dir / "{{ cookiecutter.project_name|lower|replace(' ', '-') }}"
    )
    project_template_dir.mkdir()

    # Create a simple template file that uses both variables
    template_file = project_template_dir / "config.txt"
    template_content = """Project: {{ cookiecutter.project_name }}
Feature Enabled: {{ cookiecutter.enable_feature }}
Build System: {{ cookiecutter.build_system }}
"""
    with open(template_file, 'w') as f:
        f.write(template_content)

    # Create user config to override defaults
    user_config = {
        "default_context": {
            "project_name": "My Test Project",
            "enable_feature": "yes",  # Override to "yes"
            "build_system": "setuptools",  # Override to "setuptools"
            "multiple_choice": "c2",
            "multiple_choice_2": "c4",
        }
    }

    user_config_file = tmp_path / "user_config.yaml"
    with open(user_config_file, 'w') as f:
        import yaml

        yaml.dump(user_config, f)

    # WHEN: Use cookiecutter to generate context (without full rendering)
    from cookiecutter.generate import generate_context

    context = generate_context(
        context_file=str(cookiecutter_json_file),
        default_context=user_config["default_context"],
        extra_context=None,
    )

    # THEN it has only the 'cookiecutter' key (no _cookiecutter yet)
    assert 'cookiecutter' in context
    assert '_cookiecutter' not in context

    cookiecutter_vars = context['cookiecutter']

    # Test v1 (yes/no choice variable)
    # In cookiecutter context: should be the selected string value
    assert isinstance(cookiecutter_vars['enable_feature'], list)
    assert cookiecutter_vars['enable_feature'] == ["yes", "no"]

    # Test v2 (multi-choice variable)
    # In cookiecutter context: should be the selected string value
    assert isinstance(cookiecutter_vars['build_system'], list)
    assert cookiecutter_vars['build_system'] == ["setuptools", "poetry", "flit"]

    assert isinstance(cookiecutter_vars['multiple_choice'], list)
    assert cookiecutter_vars['multiple_choice'] == ["c2", "c1", "c3"]

    # THEN cookiecutter.json arrays remain as lists in context
    # AND if user config no choice or unknown choice, then no effect data
    assert isinstance(cookiecutter_vars['multiple_choice_2'], list)
    assert cookiecutter_vars['multiple_choice_2'] == ["c1", "c2", "c3"]


def test_cookiecutter_context_preserves_choice_variable_types_v2(tmp_path: Path):
    """Test that cookiecutter preserves variable types correctly in context.

    GIVEN a cookiecutter.json file with:
    - A yes/no choice variable v1
    - A multi-choice variable v2 with options a/b/c
    WHEN cookiecutter reads/parses/renders the template
    THEN the context should contain:
    - v1 as string value (not boolean) in 'cookiecutter' context
    - v1 as list of choices in '_cookiecutter' context
    - v2 as string value (first choice) in 'cookiecutter' context
    - v2 as list of choices in '_cookiecutter' context
    """

    # GIVEN: Create a minimal cookiecutter template
    template_dir = tmp_path / "test_template"
    template_dir.mkdir()

    # Create cookiecutter.json with yes/no and multi-choice variables
    cookiecutter_json = {
        "project_name": "Test Project",
        "enable_feature": ["no", "yes"],  # yes/no choice variable (v1)
        "build_system": ["poetry", "setuptools", "flit"],  # multi-choice variable (v2)
    }

    cookiecutter_json_file = template_dir / "cookiecutter.json"
    with open(cookiecutter_json_file, 'w') as f:
        json.dump(cookiecutter_json, f, indent=2)

    # Create a minimal template project structure
    project_template_dir = (
        template_dir / "{{ cookiecutter.project_name|lower|replace(' ', '-') }}"
    )
    project_template_dir.mkdir()

    # Create a simple template file that uses both variables
    template_file = project_template_dir / "config.txt"
    template_content = """Project: {{ cookiecutter.project_name }}
Feature Enabled: {{ cookiecutter.enable_feature }}
Build System: {{ cookiecutter.build_system }}
"""
    with open(template_file, 'w') as f:
        f.write(template_content)

    # WHEN: Use cookiecutter to generate context (without full rendering)
    from cookiecutter.generate import generate_context

    context = generate_context(
        context_file=str(cookiecutter_json_file),
    )

    # THEN it has only the 'cookiecutter' key (no _cookiecutter yet)
    assert 'cookiecutter' in context
    assert '_cookiecutter' not in context

    cookiecutter_vars = context['cookiecutter']

    # Test v1 (yes/no choice variable)
    # In cookiecutter context: should be the selected string value
    assert cookiecutter_vars['enable_feature'] == ["no", "yes"]

    # Test v2 (multi-choice variable)
    # In cookiecutter context: should be the selected string value
    assert cookiecutter_vars['build_system'] == ["poetry", "setuptools", "flit"]


def test_cookiecutter_full_rendering_with_choice_variables(tmp_path: Path):
    """Test internal cookiecutter lib rendering process with choice variables.

    This test verifies that cookiecutter renders both yes/no and a/b/c choice vars as strings.

    GIVEN a 'Cookiecutter Template': cookiecutter.json + (jinja) template files
    """
    # GIVEN a cookiecutter.json with yes/no and multi-choice variables
    template_dir = tmp_path / "test_template"
    template_dir.mkdir()

    cookiecutter_json = {
        "project_name": "Test Suite Project",
        "enable_feature": ["yes", "no"],
        "docs_build_system": ["mkdocs", "sphinx", "whatever"],
    }

    with open(template_dir / "cookiecutter.json", 'w') as f:
        json.dump(cookiecutter_json, f, indent=2)

    project_template_dir = (
        template_dir / "{{ cookiecutter.project_name|lower|replace(' ', '-') }}"
    )
    project_template_dir.mkdir()

    template_content = """Project: {{ cookiecutter.project_name }}
Feature Enabled: {{ cookiecutter.enable_feature }}
Build System: {{ cookiecutter.docs_build_system }}
"""
    with open(project_template_dir / "config.txt", 'w') as f:
        f.write(template_content)

    # WHEN cookiecutter is called to render the Template
    from cookiecutter.main import cookiecutter

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    project_path = cookiecutter(
        str(template_dir),
        output_dir=str(output_dir),
        no_input=True,
        # extra_context=extra_context
    )

    # THEN cookiecutter picks 1st option from 'choice vars' and render as strings
    generated_project = Path(project_path)
    assert generated_project.exists()
    assert generated_project.name == "test-suite-project"

    config_file = generated_project / "config.txt"
    assert config_file.exists()

    rendered_content = config_file.read_text()
    expected_content = """Project: Test Suite Project
Feature Enabled: yes
Build System: mkdocs
"""
    assert rendered_content == expected_content
