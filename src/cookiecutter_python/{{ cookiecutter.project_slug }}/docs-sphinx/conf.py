# Configuration file for the Sphinx documentation builder.
#
# This file configures the readthedocs.org server that Continuously
# builds the documentation pages of the {{ cookiecutter.project_name }}
# project.

# Docstrings in the source code should be written in
# the 'Google' format.

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here
import os
import sys


def get_templated_vars():
    return type(
        'TemplatedVariables',
        (),
        dict(
            project_slug='{{ cookiecutter.project_slug }}',
            package_name='{{ cookiecutter.pkg_name }}',
            author_name='{{ cookiecutter.full_name }}',
            year='{{ cookiecutter.year }}',
            version='{{ cookiecutter.version }}',
            github_username='{{ cookiecutter.github_username }}',
            repo_name='{{ cookiecutter.repo_name }}',
        ),
    )


variables = get_templated_vars()

# Add package to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join('..', 'src', variables.package_name)))


# -- Project information -----------------------------------------------------

project = variables.project_slug
copyright = '{year}, {name}'.format(
    year=variables.year,
    name=variables.author_name,
)
author = variables.author_name

# The full version, including alpha/beta/rc tags
release = variables.version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',  # External Links Configuration: Dynamic Urls
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',  # Allow parsing of docstrings using Google format
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.spelling',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


### External Links Configuration ###
# provided by the sphinx.ext.extlinks extension

# With the current settings (see the mapping below), you can for example use the
# directive :issue:`5`, to dynamically render a link with text 'issue 5'.
# The link shall be 'clickable' and shall redirect to your issues page on github
# and specifically point to issue number 5
# https://github.com/{username}/{repository}/issues/5

# Mapping of link identifiers/keys to:
# 2-length tuples with 1st item the url and 2nd the prefix (the "text string")
# You can add etries here, according to your use case(s).
extlinks = {
    'issue': (
        'https://github.com/{username}/{repository}/issues/'.format(
            username=variables.github_username,
            repository=variables.repo_name,
        )
        + '%s',
        'issue ',
    ),
}
