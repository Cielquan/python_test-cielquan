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
import re
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
YEAR = f"{TODAY.year}"


#: -- PROJECT INFORMATION --------------------------------------------------------------

project = "python_test"
author = "Christian Riedel"
release_year = 2019
copyright = (  #: pylint: disable=W0622  # noqa:A001,VNE003
    f"{release_year}{('-' + YEAR) if YEAR != release_year else ''}, " + author
)
#: The full version, including alpha/beta/rc tags
release = __version__
#: Major version like (X.Y)
version = __version__[0:3]
#: only tags like alpha/beta/rc
release_level = re.findall(r"^[v]?\d+\.\d+\.\d+[+-]?([a-zA-Z]*)\d*", __version__)
#: Release date
release_date = f"{TODAY}"


#: -- FILES ----------------------------------------------------------------------------

source_suffix = [".rst"]

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


#: -- CONFIGS --------------------------------------------------------------------------

#: Pygments syntax highlighting style
pygments_style = "sphinx"

# rst_epilog = """
# .. |release_date| replace:: {release_date}
# .. |coverage-equals-release| replace:: coverage=={release}
# .. |doc-url| replace:: https://coverage.readthedocs.io/en/coverage-{release}
# .. |br| raw:: html
#   <br/>
# """.format(release=release, release_date=release_date)

#: Linkcheck - 1 Worker 5 Retries to fix 429 error
linkcheck_workers = 1
linkcheck_retries = 5
linkcheck_timeout = 30

tls_cacerts = os.getenv("SSL_CERT_FILE")


#: -- EXTENSIONS -----------------------------------------------------------------------

#: Default extensions
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.coverage", #: sphinx-build -b coverage ...    
]


#: -- DOCTEST --------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html
extensions.append("sphinx.ext.doctest")


#: -- IFCONFIG -------------------------------------------------------------------------
extensions.append("sphinx.ext.ifconfig")
# https://www.sphinx-doc.org/en/master/usage/extensions/ifconfig.html


#: -- VIEWCODE -------------------------------------------------------------------------
extensions.append("sphinx.ext.viewcode")


#: -- AUTOSECTIONLABEL -----------------------------------------------------------------
extensions.append("sphinx.ext.autosectionlabel")
autosectionlabel_prefix_document = True


#: -- INTERSPHINX ----------------------------------------------------------------------
extensions.append("sphinx.ext.intersphinx")
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}


#: -- EXTLINKS -------------------------------------------------------------------------
extensions.append("sphinx.ext.extlinks")
extlinks = {
    "issue": ("https://github.com/Cielquan/python_test/issues/%s", "#"),
    "pull": ("https://github.com/Cielquan/python_test/pull/%s", "pr"),
    "user": ("https://github.com/%s", "@"),
}


#: -- AUTODOC --------------------------------------------------------------------------
ext_autodoc = [
    # "sphinx.ext.autodoc",
    # "sphinx_autodoc_typehints", #: install: sphinx-autodoc-typehints
    # "sphinx_click.ext", #: install: sphinx-click
]
extensions.extend(ext_autodoc)
autodoc_member_order = "bysource"
autodoc_typehints = "signature" # TODO: 'signature' – Show typehints as its signature (default) # 'description' – Show typehints as content of function or method


def remove_module_docstring(
    app, what, name, obj, options, lines
):  # pylint: disable=R0913,W0613
    """Remove module docstring."""
    if what == "module":
        del lines[:]


#: -- HTML OUTPUT ----------------------------------------------------------------------

#: Theme
extensions.append("sphinx_rtd_theme") #: install: "sphinx-rtd-theme"
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_last_updated_fmt = TODAY.isoformat()

#: Add links to *.rst source files on HTML pages
html_show_sourcelink = True


#: -- SETUP ----------------------------------------------------------------------------

def setup(app):
    """Connect custom func to sphinx events."""
    if "sphinx.ext.autodoc" in extensions:
        app.connect("autodoc-process-docstring", remove_module_docstring)
    
    app.add_config_value('release_level', '', 'env')
