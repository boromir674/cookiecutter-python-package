import logging
import os

from .generator import generator
from .post_main import post_main
from .pre_main import pre_main

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
    print('Start Python Generator !')
    request = pre_main(
        config_file=config_file,
        default_config=default_config,
        web_servers=WEB_SERVERS,
        no_input=no_input,
        extra_context=extra_context,
    )

    project_dir = generator(
        os.path.abspath(os.path.join(my_dir, '..')),  # template dir path
        checkout=checkout,
        no_input=no_input,
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
    post_main(request)

    print('Finished :)')
    return project_dir
