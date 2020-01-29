# -*- coding: utf-8 -*-
# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'conf.py' created 2020-01-15
# is part of the project/program 'python_test'.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published by
# the Massachusetts Institute of Technology.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://opensource.org/licenses/MIT>.
#
# Github: https://github.com/Cielquan/
# ======================================================================================
"""
    docs.source.conf
    ~~~~~~~~~~~~~~~~

    Configuration file for the Sphinx documentation builder.

    :copyright: 2020 (c) Christian Riedel
    :license: MIT, see LICENSE.rst for more details
"""
import os
import sys

from pathlib import Path

from matnum import __version__


#: pylint: disable=C0103
# Paths
sys.path.insert(0, os.path.abspath("../.."))
conf_dir = Path(__file__)


# -- PROJECT INFORMATION ---------------------------------------------------------------

project = "python_test"
author = "Christian Riedel"
copyright = "2020, " + author  #: pylint: disable=W0622  #: CHANGEME
# The full version, including alpha/beta/rc tags
release = __version__
# Major version like (X.Y)
version = __version__[0:3]
# Release date
release_date = "2020"  #: CHANGEME


# -- SPHINX CONFIG ---------------------------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
]

intersphinx_mapping = {'python': ('https://docs.python.org/3/', None)}


# -- FILES -----------------------------------------------------------------------------

# Index source file
master_doc = "index"

# Files to exclude for source of doc
exclude_patterns = []

# Folder for static files, if folder exists
html_static_path = []
if Path(conf_dir, "_static").exists():
    html_static_path = ["_static"]

# Folder for template files, if folder exists
templates_path = []
if Path(conf_dir, "_templates").exists():
    templates_path = ["_templates"]


# -- HTML OUTPUT -----------------------------------------------------------------------

# Add links to *.rst source files on HTML pages
html_show_sourcelink = True

# Pygments syntax highlighting style
pygments_style = "sphinx"

# Use RTD Theme if installed
try:
    import sphinx_rtd_theme  #: pylint: disable=W0611
except ImportError:
    html_theme = "alabaster"
else:
    extensions.append("sphinx_rtd_theme")
    html_theme = "sphinx_rtd_theme"

# rst_epilog = """
# .. |release_date| replace:: {release_date}
# .. |coverage-equals-release| replace:: coverage=={release}
# .. |doc-url| replace:: https://coverage.readthedocs.io/en/coverage-{release}
# .. |br| raw:: html
#   <br/>
# """.format(release=release, release_date=release_date)

