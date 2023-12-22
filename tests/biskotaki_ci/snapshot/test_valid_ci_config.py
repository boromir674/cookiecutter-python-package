import pytest


@pytest.mark.parametrize(
    'snapshot_name',
    [
        'biskotaki-no-input',
        'biskotaki-interactive',
    ],
)
def test_snapshot_has_valid_ci_config_file_yaml(snapshot_name, test_root):
    """Test that the snapshot has a valid CI Config File"""
    from pathlib import Path

    import yaml

    # Load Snapshot
    # tests/data/snapshots/biskotaki-no-input/.github/workflows/test.yaml
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / snapshot_name
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    ### Validate .github/workflows/test.yaml ###

    # Load CI Config File
    ci_config_file: Path = snapshot_dir / '.github' / 'workflows' / 'test.yaml'
    assert ci_config_file.exists()
    assert ci_config_file.is_file()

    # Load CI Config
    ci_config: dict = yaml.safe_load(ci_config_file.read_text())
    assert ci_config

    # Check CI Config
    assert ci_config['name'] == 'CI/CD Pipeline'

    ### Validate .github/workflows/policy_lint.yml ###

    # Load CI Config File
    ci_config_file: Path = snapshot_dir / '.github' / 'workflows' / 'policy_lint.yml'
    assert ci_config_file.exists()
    assert ci_config_file.is_file()

    # Load CI Config
    ci_config: dict = yaml.safe_load(ci_config_file.read_text())
    assert ci_config
