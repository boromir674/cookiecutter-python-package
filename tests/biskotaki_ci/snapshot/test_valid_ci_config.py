import typing as t

import pytest


@pytest.mark.parametrize(
    'snapshot_name',
    [
        'biskotaki-no-input',
        'biskotaki-interactive',
    ],
)
def test_snapshot_ci_config_files_are_valid_yaml(snapshot_name, test_root):
    """Test that the snapshot has a valid CI Pipeline Config File"""
    from pathlib import Path

    import yaml

    # Load Snapshot
    # tests/data/snapshots/biskotaki-no-input/.github/workflows/test.yaml
    snapshot_dir: Path = test_root / 'data' / 'snapshots' / snapshot_name
    assert snapshot_dir.exists()
    assert snapshot_dir.is_dir()

    ### Validate .github/workflows/test.yaml ###

    # IMPORTANT: Load CI Pipeline Yaml Config File
    snapshot_2_ci_workflow: t.Dict[str, Path] = {
        # CI adopts the New Pipeline Design, as proposed in Gold Standard
        'biskotaki-no-input': snapshot_dir / '.github' / 'workflows' / 'cicd.yml',
        # Interactive also adopts the new pipeline design as default option
        'biskotaki-interactive': snapshot_dir / '.github' / 'workflows' / 'cicd.yml',
    }

    ci_config_file: Path = snapshot_2_ci_workflow[snapshot_name]
    assert ci_config_file.exists()
    assert ci_config_file.is_file()

    # Load CI Config
    import re

    def sanitize_load(text: str):
        for w in "on".split():
            reg = re.compile(r'^(on):', re.MULTILINE)
            text = reg.sub(r'\1<TEST>:', text)
        # >> Issue: [B506:yaml_load] Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load().
        # Severity: Medium   Confidence: High
        # CWE: CWE-20 (https://cwe.mitre.org/data/definitions/20.html)
        # More Info: https://bandit.readthedocs.io/en/1.7.7/plugins/b506_yaml_load.html
        return yaml.safe_load(text)

    ci_config = sanitize_load(ci_config_file.read_text())

    # ci_config: dict = yaml.safe_load(ci_config_file.read_text())
    assert ci_config
    assert isinstance(ci_config, dict)

    assert 'name' in ci_config
    assert 'on' + '<TEST>' in ci_config, 'on is missing: \n' + '\n'.join(
        [str(x) for x in ci_config.keys()]
    )
    assert 'jobs' in ci_config

    # Check CI Config
    assert ci_config['name'] == 'CI/CD Pipeline'

    ### Validate .github/workflows/policy_lint.yml ###

    # Load CI Config File
    ci_config_file = snapshot_dir / '.github' / 'workflows' / 'policy_lint.yml'
    assert ci_config_file.exists()
    assert ci_config_file.is_file()

    # Load CI Config
    ci_config = yaml.safe_load(ci_config_file.read_text())
    assert ci_config
