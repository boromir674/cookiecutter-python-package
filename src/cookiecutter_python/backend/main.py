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
    checkout=None,
    no_input=False,
    extra_context=None,
    replay=False,
    overwrite=False,
    output_dir='.',
    config_file=None,
    default_config=False,
    password=None,
    directory=None,
    skip_if_file_exists=False,
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
    #      - store 'docs' folder, per docs builder, that Generator supports
    request = pre_main(
        Request(
            config_file=config_file,
            default_config=default_config,
            web_servers=WEB_SERVERS,
            no_input=no_input,
            extra_context=extra_context,
        )
    )
    print('Extra context: ', request.extra_context)
    ## GENERATION ##
    project_dir = generator(
        os.path.abspath(os.path.join(my_dir, '..')),  # template dir path
        checkout=checkout,
        no_input=no_input,
        # we pass the Request computed context in the Cookiecutter Extra Context
        # if extra_context includes a 'supported-interpreters' key:
        #  no_input == True: automatic generation of CI Test Matrix Python Interpreters versions list, should happen
        #  no_input == False: we should first expect a Radio List Dialog to select the Python Interpreters versions list
        # then that list is passed in the Cookiecutter Extra Context, to exclude
        # "propmting for interpreters" from the set of prompts that Cookiecutter
        # is going to ask the user
        # Letting Cookiecutter ask the user for Interpreters data
        # ie 'interpreters': {"supported-interpreters": ["3.10", "3.11"]},
        # seems to result in a bug.
        # TODO:
        # Investigate if Dict[str, List[str]] is too complicated
        # for Cookiecutter to handle. And if being the case is an
        # "expected" cookiecutter behaviour.
        # then decide on whether changing data type to List[str] is needed
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
