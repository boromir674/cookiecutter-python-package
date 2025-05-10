import logging
import os

from .generator import generator
from .post_main import post_main
from .pre_main import pre_main
from .request import Request


logger = logging.getLogger(__name__)

my_dir = os.path.dirname(os.path.realpath(__file__))


WEB_SERVERS = ['pypi', 'readthedocs']


def generate(
    # interactive=True,
    no_input=False,  # INTERACTIVE ON by Default
    offline=False,
    # extra_context=None,
    replay=False,
    overwrite=False,
    output_dir='.',
    config_file=None,
    skip_if_file_exists=False,
    # deprecated
    default_config=False,
    password=None,
    directory=None,
    checkout=None,
    ###
) -> str:
    """Create Python Project, with CI/CD pipeline, from the project template.

    Generate/Scaffold a new Python Project, including configuration enabling
    automations such as CI and Continuous Delivery of Docker and Python
    'artifacts', and Continuous Documentation of the Python Project.
    """
    print('Start Python Generator !')
    # Initialize Generation Request:
    #  - store the CI Test Matrix Python Interpreters versions list
    #       -  prompt for user input in interactive or atempt to read from yaml otherwise
    #  - prepare Cookiecutter extra context:
    #      - add interpreters versions list
    request = pre_main(
        Request(
            config_file=config_file,
            default_config=default_config,
            web_servers=WEB_SERVERS,
            no_input=no_input,
            extra_context=None,
            offline=offline,
        )
    )
    print('Extra context: ', request.extra_context)
    ## GENERATION from Template; delegate to Cookiecutter callable ##
    project_dir = generator(
        os.path.abspath(os.path.join(my_dir, '..')),  # template dir path
        checkout=checkout,
        # no_input=no_input,
        no_input=True,
        extra_context=request.extra_context,
        replay=replay,
        overwrite_if_exists=overwrite,
        output_dir=output_dir,
        config_file=config_file,
        default_config=default_config,
        password=password,
        directory=directory,
        skip_if_file_exists=skip_if_file_exists,
    )
    ## POST GENERATION ##
    # Check if out-of-the-box Generated Project, coincidentally, requires slight modifications
    # for automatic and seemless "PyPI Upload" and "ReadTheDocs Build" process to
    # work. This can happen if the project name is already taken by another project
    # on PyPI or ReadTheDocs.
    post_main(request)

    print('Finished :)')
    return project_dir
