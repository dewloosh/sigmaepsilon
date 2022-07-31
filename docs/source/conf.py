# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import subprocess
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../src'))

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# -- Project information -----------------------------------------------------

project = 'SigmaEpsilon'
copyright = '2022, Bence Balogh'
author = 'Bence Balogh'

# The short X.Y version

"""here = os.path.dirname(__file__)
print('HERE : {}'.format(here))
#repo = os.path.join(here, '..', '..')
repo = os.path.abspath('../..')
print('REPO : {}'.format(repo))
print(os.path.join(repo, "/src/dewloosh"))
_module = os.listdir(os.path.join(repo, "/src/dewloosh"))[0]
_version_py = os.path.join(repo, "/src/dewloosh/{}/__init__.py".format(_module))"""

# get version from python package:
"""here = os.path.dirname(__file__)
repo = os.path.join(here, '..', '..')
_version_py = os.path.join(repo, 'src', 'sigmaepsilon', 'core', '__init__.py')
version_ns = {}
with open(_version_py) as f:
    exec(f.read(), version_ns)
# The short X.Y version.
#version = '%i.%i' % version_ns['version_info'][:2]
# The full version, including alpha/beta/rc tags.
release = version_ns['__version__']"""
    
# get version from python package:
here = os.path.dirname(__file__)
repo = os.path.join(here, '..', '..')
_version_py = os.path.join(repo, 'src', 'sigmaepsilon', 'core', '__init__.py')
release = get_version(_version_py)

try:
    git_rev = subprocess.check_output(
        ['git', 'describe', '--exact-match', 'HEAD'], universal_newlines=True)
except subprocess.CalledProcessError:
    try:
        git_rev = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], universal_newlines=True)
    except subprocess.CalledProcessError:
        git_rev = ''
if git_rev:
    git_rev = git_rev.splitlines()[0] + '/'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # allows to work with markdown files
    'myst_parser',  # pip install myst-parser for this

    # to plot summary about durations of file generations
    # 'sphinx.ext.duration',

    # to test code snippets in docstrings
    # 'sphinx.ext.doctest',

    # for automatic exploration of the source files
    'sphinx.ext.autodoc',

    # to enable cross referencing other documents on the internet
    'sphinx.ext.intersphinx',

    # Napoleon is a extension that enables Sphinx to parse both NumPy and Google style docstrings
    'sphinx.ext.napoleon',

    'nbsphinx',  # to handle jupyter notebooks
    'nbsphinx_link',  # for including notebook files from outside the sphinx source root

    'sphinx_copybutton',  # for "copy to clipboard" buttons
    'sphinx.ext.mathjax',  # for math equations
    'sphinxcontrib.bibtex',  # for bibliographic references
    'sphinxcontrib.rsvgconverter',  # for SVG->PDF conversion in LaTeX output
    'sphinx_gallery.load_style',  # load CSS for gallery (needs SG >= 0.6)

    # 'sphinx.ext.coverage',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
# source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'EN'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------


# Read The Docs
# on_rtd is whether we are on readthedocs.org, this line of code grabbed from
# docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
    # things that need to be done only locally
    pass

# otherwise, readthedocs.org uses their theme by default, so no need to specify it

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'nbsphinx-linkdoc'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
#html_title = "SigmaEpsilon"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

myst_enable_extensions = [
    "amsmath",
    "dollarmath",
]

html_title = project + ' version ' + release


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'sigmaepsilon.tex', 'SigmaEpsilon Documentation',
     'Bence Balogh', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'sigmaepsilon', 'SigmaEpsilon Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'sigmaepsilon', 'SigmaEpsilon Documentation',
     author, 'sigmaepsilon', 'One line description of project.',
     'Miscellaneous'),
]


# Ensure env.metadata[env.docname]['nbsphinx-link-target']
# points relative to repo root:
nbsphinx_link_target_root = repo


nbsphinx_prolog = (
    r"""
{% if env.metadata[env.docname]['nbsphinx-link-target'] %}
{% set docpath = env.metadata[env.docname]['nbsphinx-link-target'] %}
{% else %}
{% set docpath = env.doc2path(env.docname, base='docs/source/') %}
{% endif %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::
        This page was generated from `{{ docpath }}`__.
        
    __ https://github.com/dewloosh/sigmaepsilon/blob/
        """ +
    git_rev + r"{{ docpath }}"
)

nbsphinx_prolog = (
    r"""
{% if env.metadata[env.docname]['nbsphinx-link-target'] %}
{% set docpath = env.metadata[env.docname]['nbsphinx-link-target'] %}
{% else %}
{% set docpath = env.doc2path(env.docname, base='docs/source/') %}
{% endif %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. _this: https://github.com/dewloosh/sigmaepsilon/blob/main/{{ docpath }}
    
    .. _binder: https://github.com/dewloosh/sigmaepsilon/blob/main/{{ docpath }}
    
    .. nbinfo::
        This page was generated from 
        `{{ docpath }} <https://github.com/dewloosh/sigmaepsilon/blob/main/{{ docpath }}>`_."""
    
)
