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
#: pylint: disable=C0103
import os
import sys

from datetime import datetime
from pathlib import Path
from typing import List

import sphinx_rtd_theme  # type: ignore

from python_test import __version__


#: Add Repo to path
sys.path.insert(0, os.path.abspath("../.."))

#: Vars
CONF_DIR = Path(__file__)
TODAY = datetime.today()


#: -- PROJECT INFORMATION --------------------------------------------------------------

project = "python_test"
author = "Christian Riedel"
copyright = f"2020-{TODAY.year}, " + author  #: pylint: disable=W0622  #: CHANGEME
#: The full version, including alpha/beta/rc tags
release = __version__
#: Major version like (X.Y)
version = __version__[0:3]
#: Release date
release_date = f"{TODAY}"  #: CHANGEME


#: -- SPHINX CONFIG --------------------------------------------------------------------

#: Add any Sphinx extension module names here, as strings.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # "sphinx.ext.autodoc",
    # "sphinx_autodoc_typehints", # sphinx-autodoc-typehints
    # "sphinx_click.ext", # sphinx-click
]


#: -- LINKS ----------------------------------------------------------------------------

#: Linkcheck - 1 Worker 5 Retries to fix 429 error
linkcheck_workers = 1
linkcheck_retries = 5
linkcheck_timeout = 30

tls_cacerts = os.getenv("SSL_CERT_FILE")

intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}

extlinks = {
    "issue": ("https://github.com/Cielquan/python_test/issues/%s", "#"),
    "pull": ("https://github.com/Cielquan/python_test/pull/%s", "p"),
    "user": ("https://github.com/%s", "@"),
}


#: -- FILES ----------------------------------------------------------------------------

#: Index source file
master_doc = "index"

#: Files to exclude for source of doc
exclude_patterns: List[str] = []

#: Folder for static files, if folder exists
html_static_path = []
if Path(CONF_DIR, "_static").exists():
    html_static_path = ["_static"]

#: Folder for template files, if folder exists
templates_path = []
if Path(CONF_DIR, "_templates").exists():
    templates_path = ["_templates"]


#: -- HTML OUTPUT ----------------------------------------------------------------------

#: Theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_last_updated_fmt = TODAY.isoformat()

#: Add links to *.rst source files on HTML pages
html_show_sourcelink = True

#: Pygments syntax highlighting style
pygments_style = "sphinx"

# rst_epilog = """
# .. |release_date| replace:: {release_date}
# .. |coverage-equals-release| replace:: coverage=={release}
# .. |doc-url| replace:: https://coverage.readthedocs.io/en/coverage-{release}
# .. |br| raw:: html
#   <br/>
# """.format(release=release, release_date=release_date)
