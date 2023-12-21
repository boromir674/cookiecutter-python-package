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


    ## Logging file created - Assertions ##
    from cookiecutter_python._logging_config import FILE_TARGET_LOGS

    # Expected and Intentend Logging behaviour:
    # - log file with records is created in PWD of the shell that runs the generator

    # get pwd of the shell that runs the generator
    pwd = Path.cwd()
    INTENTIONALLY_PLACED_LOG_FILE: Path = pwd / FILE_TARGET_LOGS
    assert INTENTIONALLY_PLACED_LOG_FILE.exists()
    # AND has at least some Log records captured, during runtime code execution
    assert INTENTIONALLY_PLACED_LOG_FILE.is_file()
    # assert INTENTIONALLY_PLACED_LOG_FILE.stat().st_size > 0

    ###### Document kind of Bug ######
    # Expected but probably unintented behaviour:
    # - empty log file gets created inside the gen project dir

    # Log file is placed inside the generated project dir, after generation
    # probably it should be place in PWD of the shell that runs the generator

    FIXED = True
    fixed_unintentional_placement_of_log_file_in_gen_proj_dir: bool = FIXED
    bug = not fixed_unintentional_placement_of_log_file_in_gen_proj_dir
    
    UNINTENTIONALLY_PLACED_LOG_FILE: Path = gen_project_dir / FILE_TARGET_LOGS
    assert not bug
    ## Implementation Option 1
    if bug:
        print(f"\n Verifying Unintentional Logging Behaviour still happens: {bug}\n")
        assert UNINTENTIONALLY_PLACED_LOG_FILE.exists()
        assert UNINTENTIONALLY_PLACED_LOG_FILE.is_file()
        assert UNINTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
    else:
        assert not UNINTENTIONALLY_PLACED_LOG_FILE.exists()
    ## Implementation Option 2
    # assert (
    #     not bug and not UNINTENTIONALLY_PLACED_LOG_FILE.exists()
    # ) or (
    #     bug and UNINTENTIONALLY_PLACED_LOG_FILE.exists() and UNINTENTIONALLY_PLACED_LOG_FILE.is_file() and UNINTENTIONALLY_PLACED_LOG_FILE.stat().st_size == 0
    # )

    ##################################

    return gen_project_dir
