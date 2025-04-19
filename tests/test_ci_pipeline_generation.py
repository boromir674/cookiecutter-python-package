import pytest


@pytest.mark.parametrize(
    'config_file',
    [
        # Test Case 1
        # '.github/biskotaki.yaml',
        # Test Case 2
        None,
    ],
)
def test_file_is_valid_yaml(config_file, user_config, mock_check, tmpdir):
    """Test Generator produces Valid CI config files, as expected.

    This Test features the following:
      - automatically mocks futures (web/http)
    """
    from pathlib import Path

    # user_config_file: Path = Path(__file__).parent / '..' / config_file
    # Generate the pipeline
    from cookiecutter_python.backend.main import generate

    default_parameters = user_config[config_file]
    mock_check.config = default_parameters
    mock_check('pypi', True)
    mock_check('readthedocs', True)

    project_dir: str = generate(
        no_input=True,
        output_dir=tmpdir,
        config_file=config_file,
        default_config=False,
    )

    generate_ci_pipeline_config = Path(project_dir) / '.github' / 'workflows' / 'test.yaml'
    assert generate_ci_pipeline_config.exists()
    assert generate_ci_pipeline_config.is_file()

    # Assert that the pipeline is valid yaml
    import re

    import yaml

    def sanitize_load(s: str):
        for w in "on".split():
            reg = re.compile(r'^(on):', re.MULTILINE)
            s = reg.sub(r'\1<TEST>:', s)
        # >> Issue: [B506:yaml_load] Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load().
        # Severity: Medium   Confidence: High
        # CWE: CWE-20 (https://cwe.mitre.org/data/definitions/20.html)
        # More Info: https://bandit.readthedocs.io/en/1.7.7/plugins/b506_yaml_load.html
        return yaml.safe_load(s)

    ci_config = sanitize_load(generate_ci_pipeline_config.read_text())

    assert ci_config is not None
    assert isinstance(ci_config, dict)

    assert 'name' in ci_config
    assert 'on' + '<TEST>' in ci_config, 'on is missing: \n' + '\n'.join(
        [str(x) for x in ci_config.keys()]
    )
    assert 'jobs' in ci_config

    assert 'test_suite' in ci_config['jobs']
    assert 'pypi_publish' in ci_config['jobs']
    assert 'check_which_git_branch_we_are_on' in ci_config['jobs']
    assert 'docker_build' in ci_config['jobs']
