# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import typing

# -- Path setup --------------------------------------------------------------


sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'bloom'
copyright = '2021, A5rocks'
author = 'A5rocks'

import bloom  # noqa: E402

version = bloom.__version__
release = version


# -- General configuration ---------------------------------------------------


# silently failing is BAD.
nitpicky = True

# taken from trio's docs
autodoc_inherit_docstrings = False
default_role = 'obj'
autodoc_member_order = 'bysource'
pygments_style = 'default'
highlight_language = 'python3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinxcontrib_trio'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'trio': ('https://trio.readthedocs.io/en/latest/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: typing.List[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
