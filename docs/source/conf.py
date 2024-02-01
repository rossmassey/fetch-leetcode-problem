import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'rossmassey.fetch-leetcode-problem'
copyright = '2024, Ross Massey'
author = 'Ross Massey'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',   # html generation from docstrings
    'sphinx.ext.viewcode',  # source code in documentation
    'sphinx.ext.napoleon'
]


templates_path = ['_templates']
exclude_patterns = []

# modules location
sys.path.insert(0, os.path.abspath('../../'))

# only show final name (x instead of src.x)
add_module_names = False

# do not sort alphabetically
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'python_docs_theme'
html_static_path = ['_static']

# add css
html_css_files = ['css/custom.css']

def skip(app, what, name, obj, would_skip, options):
    """
    Allows the __init__ method to be autodoc
    """
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.add_css_file('css/custom.css')
    app.connect("autodoc-skip-member", skip)
