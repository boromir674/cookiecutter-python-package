"""Test for interactive CLI bug with derived fields from config file."""

from unittest.mock import patch

import yaml


def test_derived_fields_show_config_values_in_interactive_mode(tmp_path):
    """Test that derived fields show config file values in interactive mode.

    GIVEN User used --config-file CLI flag with a valid YAML config
    WHEN the config YAML file includes derived fields like "pkg_name" that come after "project_name"
    THEN in interactive CLI the value from config YAML is displayed for "pkg_name"
    AND NOT the computed value derived from project_name transformation
    """
    # Create a config file with explicit project_slug (minimal config on purpose)
    config_data = {
        'default_context': {
            'project_slug': 'custom-package-name',  # This should override derived value
            'initialize_git_repo': 'no',
        }
    }

    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(yaml.dump(config_data))

    # Parse context with config file (simulating what happens in interactive mode)
    from cookiecutter_python.backend.helpers import parse_context

    # Mock the interactive pipeline to capture what values are passed to it
    captured_context = None

    def mock_process(self, context_list):
        nonlocal captured_context
        # Capture the dictionary that would be passed to interactive dialogs
        captured_context = context_list[0]  # First item is the context dict for dialogs
        return context_list

    # Replace the real InteractiveDialogsPipeline.process with our mock
    with patch(
        'cookiecutter_python.backend.helpers.InteractiveDialogsPipeline.process', mock_process
    ):
        parse_context(str(config_file))

    # The captured context should contain the config file value for pkg_name
    assert captured_context is not None, "Context should have been captured"
    print("Captured context:", captured_context)
    # Check that project_slug is present in the captured context
    # This is the bug - currently project_slug is not included in the context passed to dialogs
    assert 'project_slug' in captured_context, (
        "project_slug should be included in context passed to interactive dialogs. "
        "Current implementation in helpers.py only includes subset of fields."
    )

    # The value should be from config file, not derived from project_name
    expected_project_slug = 'custom-package-name'  # From config file

    assert captured_context['project_slug'] == expected_project_slug, (
        f"Expected project_slug from config file '{expected_project_slug}', "
        f"but got derived value '{captured_context.get('project_slug', 'NOT_FOUND')}'"
    )


def test_derived_fields_fallback_to_computed_values_when_not_in_config(tmp_path):
    """Test that derived fields fallback to computed values when not in config.

    GIVEN User used --config-file CLI flag with a valid YAML config
    WHEN the config YAML file does NOT include derived fields like "pkg_name"
    THEN in interactive CLI the computed/derived value is displayed for "pkg_name"
    """
    # Create a config file WITHOUT pkg_name
    config_data = {
        'default_context': {
            'project_name': 'My Test Project',
            'project_type': 'module',
            # Note: pkg_name is NOT specified
            'full_name': 'Test User',
            'author_email': 'test@example.com',
            'github_username': 'testuser',
            'project_short_description': 'A test project',
            'version': '1.0.0',
            'initialize_git_repo': 'no',
            'docs_builder': 'sphinx',
            'rtd_python_version': '3.10',
            'cicd': 'stable',
        }
    }

    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(yaml.dump(config_data))

    # Parse context with config file
    from cookiecutter_python.backend.helpers import parse_context

    captured_context = None

    def mock_process(self, context_list):
        nonlocal captured_context
        # Capture the dictionary that would be passed to interactive dialogs
        captured_context = context_list[0]  # First item is the context dict for dialogs
        return context_list

    # Replace the real InteractiveDialogsPipeline.process with our mock
    with patch(
        'cookiecutter_python.backend.helpers.InteractiveDialogsPipeline.process', mock_process
    ):
        parse_context(str(config_file))

    # pkg_name should still be available and have derived value
    assert captured_context is not None

    # Even when not in config, pkg_name should be in context for the dialog
    assert (
        'pkg_name' in captured_context
    ), "pkg_name should be available in context even when not in config file"

    # Should be the derived value since not in config - but the dialog lambda will compute it
    # The lambda function in the dialog will compute: 'my-test-project'.replace('-', '_') = 'my_test_project'
    # But since we're mocking the dialog, we expect the context to contain the lambda function,
    # not the pre-computed value. The actual computation happens in the real dialog.

    # For this test, we verify that pkg_name has the empty fallback (indicating no user config)
    # and the dialog system will use the lambda to compute the value when actually running
    assert captured_context['pkg_name'] == '', (
        f"Expected empty pkg_name to trigger lambda computation, "
        f"but got '{captured_context.get('pkg_name', 'NOT_FOUND')}'"
    )


def test_all_cookiecutter_json_fields_available_in_interactive_context(tmp_path):
    """Test that all cookiecutter.json fields are available in interactive context.

    GIVEN the cookiecutter.json defines various fields including derived ones
    WHEN parsing context for interactive mode
    THEN all fields should be available in the context passed to dialogs
    """
    # Basic config with just required fields
    config_data = {
        'default_context': {
            'project_name': 'Test Project',
            'project_type': 'module',
            'full_name': 'Test User',
            'author_email': 'test@example.com',
            'github_username': 'testuser',
            'project_short_description': 'A test project',
            'version': '1.0.0',
            'initialize_git_repo': 'no',
            'docs_builder': 'sphinx',
            'rtd_python_version': '3.10',
            'cicd': 'stable',
        }
    }

    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(yaml.dump(config_data))

    # Parse context
    from cookiecutter_python.backend.helpers import parse_context

    captured_context = None

    def mock_process(self, context_list):
        nonlocal captured_context
        # Capture the dictionary that would be passed to interactive dialogs
        captured_context = context_list[0]  # First item is the context dict for dialogs
        return context_list

    # Replace the real InteractiveDialogsPipeline.process with our mock
    with patch(
        'cookiecutter_python.backend.helpers.InteractiveDialogsPipeline.process', mock_process
    ):
        parse_context(str(config_file))

    # All derived fields should be in context
    derived_fields = [
        'project_slug',
        'pkg_name',
        'repo_name',
        'readthedocs_project_slug',
        'docker_image',
        'author',  # derived from full_name
        'pypi_subtitle',  # derived from project_short_description
    ]

    for field in derived_fields:
        assert field in captured_context, (
            f"Derived field '{field}' should be available in interactive context. "
            f"Available fields: {list(captured_context.keys())}"
        )
