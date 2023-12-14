from pathlib import Path

import pytest


@pytest.fixture
def biskotaki_ci_project(
    # Mock Network Code, to prevent http (future) requests
    user_config,
    mock_check,
    test_root,
    tmp_path,
) -> Path:
    """Fixture that generates a project from .github/biskotaki.yaml"""
    from cookiecutter_python.backend.main import generate

    assert test_root.exists()
    assert test_root.is_dir()
    assert test_root.name == 'tests'
    assert test_root.is_absolute()

    biskotaki_yaml: Path = test_root.parent / '.github' / 'biskotaki.yaml'
    assert biskotaki_yaml.exists()
    assert biskotaki_yaml.is_file()
    assert biskotaki_yaml.name == 'biskotaki.yaml'

    # Mock Network Code, in case http (Future) requests are made
    mock_check.config = user_config[biskotaki_yaml]
    mock_check('pypi', True)
    mock_check('readthedocs', True)

    # Generate Biskota from CI Config Yaml
    project_dir: str = generate(
        no_input=True,
        output_dir=tmp_path,  # Path or string to a folder path
        config_file=str(biskotaki_yaml),  # better be a string
        default_config=False,
    )
    gen_project_dir: Path = Path(project_dir)

    # Sanity Checks
    assert gen_project_dir.exists()
    assert gen_project_dir.is_dir()
    assert (gen_project_dir / 'src').exists() and (gen_project_dir / 'src').is_dir()

    return gen_project_dir
