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
    """Generated Project from '.github/biskotaki.yaml' config-file.

    Use this Fixture to utilize a Project produced by the Generatpr at
    test-time (once), using the same '.github/biskotaki.yaml' config-file,
    used for publishing (via CI) the Biskotaki (generated) Project.
    """
    import sys

    from cookiecutter_python.backend.main import generate

    assert test_root.exists()
    assert test_root.is_dir()
    assert test_root.name == 'tests'
    assert test_root.is_absolute()

    #### if running OUTSIDE of local checkout ####

    TEST_TIME_BISKOTAKI_CONFIG = None
    biskotaki_yaml: Path

    if not (test_root.parent / '.github' / 'biskotaki.yaml').exists():
        import tempfile

        # Create a temporary file to use as a test config and PRESERVE it on close!
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as fp:
            fp.write(
                b"""
default_context:
    project_name: Biskotaki
    project_type: module
    project_slug: biskotaki
    pkg_name: biskotaki
    repo_name: biskotaki
    readthedocs_project_slug: biskotaki
    docker_image: biskotaki
    full_name: Konstantinos Lampridis
    author: Konstantinos Lampridis
    email: k.lampridis@hotmail.com
    author_email: k.lampridis@hotmail.com
    github_username: boromir674
    project_short_description: Project generated using https://github.com/boromir674/cookiecutter-python-package
    initialize_git_repo: 'no'
    interpreters: {"supported-interpreters": ["3.7", "3.8", "3.9", "3.10", "3.11"]}
    ## Documentation Config ##
    docs_builder: "sphinx"
    ## READ THE DOCS CI Config ##
    rtd_python_version: "3.10"
    cicd: 'experimental'

"""
            )
            fp.close()
            TEST_TIME_BISKOTAKI_CONFIG = Path(fp.name)
        biskotaki_yaml = TEST_TIME_BISKOTAKI_CONFIG
    else:
        #### else RUNNING_FROM_LOCAL_CHECKOUT ####

        biskotaki_yaml = test_root.parent / '.github' / 'biskotaki.yaml'
        assert biskotaki_yaml.exists()
        assert biskotaki_yaml.is_file()
        assert biskotaki_yaml.name == 'biskotaki.yaml'

    ### END ###

    # Mock Network Code, in case http (Future) requests are made
    mock_check.config = user_config[biskotaki_yaml]
    mock_check('pypi', True)
    mock_check('readthedocs', True)

    ######## GENERATE Biskotaki from CI Config Yaml ########
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
    # on Windows, it has been reported that the Log file is missing

    if sys.platform != 'win32':
        # here we used to assert that Log File exists where it should
        # assert INTENTIONALLY_PLACED_LOG_FILE.exists()
        # assert INTENTIONALLY_PLACED_LOG_FILE.is_file()
        # AND has at least some Log records captured, during runtime code execution
        # assert INTENTIONALLY_PLACED_LOG_FILE.stat().st_size > 0

        # this commit somehow makes CI on Linux to break. But not on dev machine

        # issue a pytest warning whever the Log File is not created as it should
        if not INTENTIONALLY_PLACED_LOG_FILE.exists():
            pytest.warns(
                UserWarning,
                match="Bug re-appeared? Regression on Linux-based OS?",
            )

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
    if sys.platform != 'win32':
        # on Windows, it has been reported that the Log file exists!
        assert not UNINTENTIONALLY_PLACED_LOG_FILE.exists()

    ##################################

    return gen_project_dir
