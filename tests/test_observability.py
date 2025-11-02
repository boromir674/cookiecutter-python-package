"""Test observability integration with the cookiecutter template.

This test suite validates that the observability stack (Grafana + Loki + Promtail)
is correctly integrated into generated projects when the include_observability
parameter is set to 'yes'.
"""

import os
import tempfile
import typing as t
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def generate_test_project():
    """Helper fixture to generate a test project with observability configuration.

    Returns a function that can be called with specific parameters to generate
    a project for testing purposes.
    """
    temp_dirs = []  # Keep track of temp directories to clean up

    def _generate_test_project(
        include_observability: str = "yes",
        project_type: str = "module",
        config_extra: t.Optional[t.Dict[str, str]] = None,
    ) -> str:
        from cookiecutter_python.backend.main import generate

        # Create temporary directory but don't auto-clean it yet
        temp_dir = tempfile.mkdtemp()
        temp_dirs.append(temp_dir)

        config_file = os.path.join(temp_dir, 'test_config.yaml')

        # Generate unique project name to avoid collisions
        project_name = 'Unit Test Observability Project'

        # Base configuration
        config = {
            'default_context': {
                'project_name': project_name,
                'include_observability': include_observability,
                'project_type': project_type,
                'cli_entry_point': 'test_observability',
                'repo_hosting_domain': 'github.com',
                'interpreters': {"supported-interpreters": ["3.8", "3.9", "3.10", "3.11"]},
            }
        }

        # Add any extra configuration
        if config_extra:
            config['default_context'].update(config_extra)

        # Write config file
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        # Generate project
        output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)

        return generate(
            config_file=config_file, output_dir=output_dir, no_input=True, offline=True
        )

    yield _generate_test_project

    # Cleanup temporary directories after test
    import shutil

    for temp_dir in temp_dirs:
        try:
            shutil.rmtree(temp_dir)
        except OSError:
            pass  # Ignore cleanup errors


def test_observability_directory_created_when_enabled(
    # GIVEN a project generator configured with observability enabled
    generate_test_project,
):
    # WHEN we generate a project with include_observability set to 'yes'
    project_path = generate_test_project(include_observability="yes")
    obs_dir = Path(project_path) / 'observability'

    # THEN the observability directory should be created
    assert obs_dir.exists(), "Observability directory should exist when enabled"
    assert obs_dir.is_dir(), "Observability path should be a directory"


def test_observability_directory_not_created_when_disabled(
    # GIVEN a project generator configured with observability disabled
    generate_test_project,
):
    # WHEN we generate a project with include_observability set to 'no'
    project_path = generate_test_project(include_observability="no")
    obs_dir = Path(project_path) / 'observability'

    # THEN the observability directory should not be created
    assert not obs_dir.exists(), "Observability directory should not exist when disabled"


def test_docker_compose_observability_file_exists(
    # GIVEN a project generator with observability enabled
    generate_test_project,
):
    # WHEN we generate a project with observability stack
    project_path = generate_test_project(include_observability="yes")
    docker_compose_file = (
        Path(project_path) / 'observability' / 'docker-compose.observability.yml'
    )

    # THEN the docker-compose observability file should be created
    assert docker_compose_file.exists(), "docker-compose.observability.yml should exist"
    assert docker_compose_file.is_file(), "docker-compose.observability.yml should be a file"


def test_loki_config_file_exists(
    # GIVEN a project generator with observability enabled
    generate_test_project,
):
    # WHEN we generate a project with observability stack
    project_path = generate_test_project(include_observability="yes")
    loki_config = Path(project_path) / 'observability' / 'loki' / 'loki-config.yml'

    # THEN the Loki configuration file should be created
    assert loki_config.exists(), "loki-config.yml should exist"
    assert loki_config.is_file(), "loki-config.yml should be a file"


def test_promtail_config_file_exists(
    # GIVEN a project generator with observability enabled
    generate_test_project,
):
    # WHEN we generate a project with observability stack
    project_path = generate_test_project(include_observability="yes")
    promtail_config = Path(project_path) / 'observability' / 'promtail' / 'promtail-config.yml'

    # THEN the Promtail configuration file should be created
    assert promtail_config.exists(), "promtail-config.yml should exist"
    assert promtail_config.is_file(), "promtail-config.yml should be a file"


def test_grafana_datasource_config_exists(
    # GIVEN a project generator with observability enabled
    generate_test_project,
):
    # WHEN we generate a project with observability stack
    project_path = generate_test_project(include_observability="yes")
    datasource_config = (
        Path(project_path) / 'observability' / 'grafana' / 'datasources' / 'loki.yml'
    )

    # THEN the Grafana datasource configuration should be created
    assert datasource_config.exists(), "Grafana loki.yml should exist"
    assert datasource_config.is_file(), "Grafana loki.yml should be a file"


def test_observability_readme_exists(
    # GIVEN a project generator with observability enabled
    generate_test_project,
):
    # WHEN we generate a project with observability stack
    project_path = generate_test_project(include_observability="yes")
    readme_file = Path(project_path) / 'observability' / 'README.md'

    # THEN the observability README documentation should be created
    assert readme_file.exists(), "Observability README.md should exist"
    assert readme_file.is_file(), "Observability README.md should be a file"


def test_docker_compose_has_valid_yaml_syntax(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we check the generated docker-compose file
    project_path = generate_test_project(include_observability="yes")
    docker_compose_file = (
        Path(project_path) / 'observability' / 'docker-compose.observability.yml'
    )

    # THEN the file should have valid YAML syntax
    with open(docker_compose_file, 'r') as f:
        yaml.safe_load(f)  # Should not raise an exception if YAML is valid


def test_loki_config_has_valid_yaml_syntax(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we check the generated Loki configuration file
    project_path = generate_test_project(include_observability="yes")
    loki_config = Path(project_path) / 'observability' / 'loki' / 'loki-config.yml'

    # THEN the file should have valid YAML syntax
    with open(loki_config, 'r') as f:
        yaml.safe_load(f)  # Should not raise an exception if YAML is valid


def test_promtail_config_has_valid_yaml_syntax(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we check the generated Promtail configuration file
    project_path = generate_test_project(include_observability="yes")
    promtail_config = Path(project_path) / 'observability' / 'promtail' / 'promtail-config.yml'

    # THEN the file should have valid YAML syntax
    with open(promtail_config, 'r') as f:
        yaml.safe_load(f)  # Should not raise an exception if YAML is valid


def test_grafana_datasource_has_valid_yaml_syntax(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we check the generated Grafana datasource configuration
    project_path = generate_test_project(include_observability="yes")
    datasource_config = (
        Path(project_path) / 'observability' / 'grafana' / 'datasources' / 'loki.yml'
    )

    # THEN the file should have valid YAML syntax
    with open(datasource_config, 'r') as f:
        yaml.safe_load(f)  # Should not raise an exception if YAML is valid


def test_docker_compose_contains_project_specific_names(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we examine the docker-compose file content
    project_path = generate_test_project(include_observability="yes")
    docker_compose_file = (
        Path(project_path) / 'observability' / 'docker-compose.observability.yml'
    )
    content = docker_compose_file.read_text()

    # Extract the actual project slug from the generated project path
    project_slug = Path(project_path).name

    # THEN it should contain project-specific container names
    assert (
        f'{project_slug}-grafana' in content
    ), f"Should contain project-specific Grafana container name with slug: {project_slug}"
    assert (
        f'{project_slug}-loki' in content
    ), f"Should contain project-specific Loki container name with slug: {project_slug}"
    assert (
        f'{project_slug}-promtail' in content
    ), f"Should contain project-specific Promtail container name with slug: {project_slug}"


def test_observability_works_with_different_project_types(
    # GIVEN different project types supported by the generator
    generate_test_project,
):
    project_types = ["module", "module+cli", "pytest-plugin"]

    for project_type in project_types:
        # WHEN we generate a project of each type with observability enabled
        project_path = generate_test_project(
            include_observability="yes", project_type=project_type
        )
        obs_dir = Path(project_path) / 'observability'

        # THEN the observability stack should be generated for all project types
        assert obs_dir.exists(), f"Observability should work with {project_type} projects"


def test_loki_config_contains_expected_content(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we examine the Loki configuration content
    project_path = generate_test_project(include_observability="yes")
    loki_config = Path(project_path) / 'observability' / 'loki' / 'loki-config.yml'

    with open(loki_config, 'r') as f:
        config = yaml.safe_load(f)

    # THEN it should contain all required Loki configuration sections
    assert 'auth_enabled' in config, "Loki config should have auth_enabled setting"
    assert 'server' in config, "Loki config should have server section"
    assert 'common' in config, "Loki config should have common section"
    assert 'schema_config' in config, "Loki config should have schema_config section"
    assert 'limits_config' in config, "Loki config should have limits_config section"
    assert 'schema_config' in config, "Loki config should have schema_config section"


def test_promtail_config_contains_expected_content(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we examine the Promtail configuration content
    project_path = generate_test_project(include_observability="yes")
    promtail_config = Path(project_path) / 'observability' / 'promtail' / 'promtail-config.yml'

    with open(promtail_config, 'r') as f:
        config = yaml.safe_load(f)

    # THEN it should contain all required Promtail configuration sections
    assert 'server' in config, "Promtail config should have server section"
    assert 'clients' in config, "Promtail config should have clients section"
    assert 'scrape_configs' in config, "Promtail config should have scrape_configs section"


def test_grafana_datasource_points_to_loki(
    # GIVEN a project with observability stack generated
    generate_test_project,
):
    # WHEN we examine the Grafana datasource configuration
    project_path = generate_test_project(include_observability="yes")
    datasource_config = (
        Path(project_path) / 'observability' / 'grafana' / 'datasources' / 'loki.yml'
    )

    with open(datasource_config, 'r') as f:
        config = yaml.safe_load(f)

    # THEN it should be properly configured to connect to the Loki service
    datasources = config.get('datasources', [])
    assert len(datasources) > 0, "Should have at least one datasource"

    loki_datasource = datasources[0]
    assert loki_datasource['type'] == 'loki', "Datasource should be of type 'loki'"
    assert (
        'loki:3100' in loki_datasource['url']
    ), "Should point to Loki service on standard port"
    assert loki_datasource['name'] == 'Loki', "Should have proper display name"
    assert loki_datasource['isDefault'] is True, "Should be the default datasource"
