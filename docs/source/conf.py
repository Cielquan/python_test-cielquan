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
from typing import List, Optional

import sphinx_rtd_theme  # type: ignore

from python_test import __version__  # CHANGE ME

sys.path.insert(0, str(Path(__file__).parents[2]))  #: Add Repo to path
needs_sphinx = "2.0"  #: Minimum Sphinx version to build the docs


#: -- GLOB VARS ------------------------------------------------------------------------
CONF_DIR = Path(__file__)
TODAY = datetime.today()
YEAR = f"{TODAY.year}"


#: -- UTILS ----------------------------------------------------------------------------
def get_release_level(version: str) -> Optional[str]:
    """Extract release tag from version string"""
    tag = re.search(r"^[v]?\d+\.\d+\.\d+[+-]?([a-zA-Z]*)\d*", version)
    if tag:
        return tag.group(1)
    return ""


#: -- PROJECT INFORMATION --------------------------------------------------------------
project = "python_test"  # CHANGE ME
author = "Christian Riedel"  # CHANGE ME
RELEASE_YEAR = 2019  # CHANGE ME
RELEASE_DATE = f"{TODAY}"
copyright = (  #: pylint: disable=W0622  # noqa:A001,VNE003
    f"{RELEASE_YEAR}{('-' + YEAR) if YEAR != RELEASE_YEAR else ''}, " + author
)
release = __version__  #: The full version, including alpha/beta/rc tags
version = __version__[0:3]  #: Major + Minor version like (X.Y)
RELEASE_LEVEL = get_release_level(__version__)  #: only tags like alpha/beta/rc


#: -- GENERAL CONFIG -------------------------------------------------------------------
extensions = []
today = TODAY.isoformat()
today_fmt = "%Y-%m-%d"
exclude_patterns: List[str] = []  #: Files to exclude for source of doc

#: Added dirs for static and template files if they exist
html_static_path = ["_static"] if Path(CONF_DIR, "_static").exists() else []
templates_path = ["_templates"] if Path(CONF_DIR, "_templates").exists() else []

rst_epilog = f"""
.. |release_date| replace:: {RELEASE_DATE}
.. |br| raw:: html

  <br/>
"""

tls_cacerts = os.getenv("SSL_CERT_FILE")


#: -- LINKCHECK CONFIG -----------------------------------------------------------------
#: 1 Worker 5 Retries to fix 429 error
linkcheck_workers = 1
linkcheck_retries = 5
linkcheck_timeout = 30


#: -- DEFAULT EXTENSIONS ---------------------------------------------------------------
extensions.append("sphinx.ext.duration")
extensions.append("sphinx.ext.coverage")  #: sphinx-build -b coverage ...


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
ext_autodoc: List[str] = [
    # "sphinx.ext.autodoc",
    # "sphinx_autodoc_typehints", #: needs install: sphinx-autodoc-typehints
    # "sphinx_click.ext", #: needs install: sphinx-click
]
extensions.extend(ext_autodoc)
autodoc_member_order = "bysource"
autodoc_typehints = "signature"  # TODO: 'signature' – Show typehints as its signature (default) # 'description' – Show typehints as content of function or method


def remove_module_docstring(
    app, what, name, obj, options, lines
):  # pylint: disable=R0913,W0613
    """Remove module docstring."""
    if what == "module":
        del lines[:]


#: -- HTML OUTPUT ----------------------------------------------------------------------
extensions.append("sphinx_rtd_theme")  #: needs install: "sphinx-rtd-theme"
html_theme = "sphinx_rtd_theme"
html_theme_options = {"style_external_links": True}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_last_updated_fmt = today_fmt
html_show_sourcelink = True  #: Add links to *.rst source files on HTML pages


#: -- LaTeX OUTPUT ---------------------------------------------------------------------



#: -- FINAL SETUP ----------------------------------------------------------------------
def setup(app):
    """Connect custom func to sphinx events."""
    if "sphinx.ext.autodoc" in extensions:
        app.connect("autodoc-process-docstring", remove_module_docstring)

    app.add_config_value("RELEASE_LEVEL", "", "env")
