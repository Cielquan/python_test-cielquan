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

from datetime import date
from pathlib import Path
from typing import List, Optional

import sphinx_rtd_theme  # type: ignore

from python_test import __version__  # CHANGE ME


sys.path.insert(0, str(Path(__file__).parents[2]))  #: Add Repo to path
needs_sphinx = "3.0"  #: Minimum Sphinx version to build the docs


#: -- GLOB VARS ------------------------------------------------------------------------
CONF_DIR = Path(__file__)
YEAR = f"{date.today().year}"


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
copyright = (  #: pylint: disable=W0622  # noqa:A001,VNE003
    f"{RELEASE_YEAR}{('-' + YEAR) if YEAR != RELEASE_YEAR else ''}, " + author
)
release = __version__  #: The full version, including alpha/beta/rc tags
version = __version__[0:3]  #: Major + Minor version like (X.Y)
RELEASE_LEVEL = get_release_level(__version__)  #: only tags like alpha/beta/rc


#: -- GENERAL CONFIG -------------------------------------------------------------------
extensions = []
today_fmt = "%Y-%m-%d"
exclude_patterns: List[str] = []  #: Files to exclude for source of doc

#: Added dirs for static and template files if they exist
html_static_path = ["_static"] if Path(CONF_DIR, "_static").exists() else []
templates_path = ["_templates"] if Path(CONF_DIR, "_templates").exists() else []

rst_prolog = f"""
.. ifconfig:: RELEASE_LEVEL in ('alpha', 'beta', 'rc')

   .. warning::
      The here documented release |release| is a prerelease.
      Keep in mind that breaking changes can occur till the final release.

      You may want to use the latest stable release instead.
"""

rst_epilog = """
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
#: Global
extensions.append("sphinx.ext.duration")
extensions.append("sphinx.ext.coverage")  #: sphinx-build -b coverage ...
coverage_write_headline = False
coverage_show_missing_items = True
extensions.append("sphinx.ext.doctest")  #: sphinx-build -b doctest ...

#: ReStructuredText
extensions.append("sphinx.ext.autosectionlabel")
autosectionlabel_prefix_document = True
extensions.append("sphinx.ext.ifconfig")
extensions.append("sphinx.ext.viewcode")

#: Links
extensions.append("sphinx.ext.intersphinx")
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}

extensions.append("sphinx.ext.extlinks")
extlinks = {
    "issue": ("https://github.com/Cielquan/python_test/issues/%s", "#"),  # CHANGE ME
    "pull": ("https://github.com/Cielquan/python_test/pull/%s", "pr"),  # CHANGE ME
    "user": ("https://github.com/%s", "@"),
}


#: -- APIDOC ---------------------------------------------------------------------------
try:
    import sphinxcontrib.apidoc  # type: ignore
except ModuleNotFoundError:
    print("## 'sphinxcontrib-apidoc' extension not loaded - not installed")
else:
    extensions.append("sphinxcontrib.apidoc")
apidoc_separate_modules = True
apidoc_module_first = True


#: -- AUTODOC --------------------------------------------------------------------------
extensions.append("sphinx.ext.autodoc")
autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_mock_imports: List[str] = []
autodoc_default_options = {"members": True}

try:
    import sphinx_autodoc_typehints  # type: ignore
except ModuleNotFoundError:
    print("## 'sphinx-autodoc-typehints' extension not loaded - not installed")
else:
    extensions.append("sphinx_autodoc_typehints")


def remove_module_docstring(
    app, what, name, obj, options, lines
):  # pylint: disable=R0913,W0613
    """Remove module docstring."""
    if what == "module":
        del lines[:]


#: -- CLICK ----------------------------------------------------------------------------
try:
    import sphinx_click.ext  # type: ignore
except ModuleNotFoundError:
    print("## 'sphinx-click' extension not loaded - not installed")
else:
    extensions.append("sphinx_click.ext")


#: -- HTML THEME -----------------------------------------------------------------------
#: needs install: "sphinx-rtd-theme"
extensions.append("sphinx_rtd_theme")
html_theme = "sphinx_rtd_theme"
html_theme_options = {"style_external_links": True}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


#: -- HTML OUTPUT ----------------------------------------------------------------------
html_last_updated_fmt = today_fmt
html_show_sourcelink = True  #: Add links to *.rst source files on HTML pages
html_logo = None  # CHANGE ME
html_favicon = None  # CHANGE ME


#: -- LaTeX OUTPUT ---------------------------------------------------------------------
latex_logo = html_logo
latex_show_pagerefs = True
latex_show_urls = "footnote"


#: -- FINAL SETUP ----------------------------------------------------------------------
def setup(app):
    """Connect custom func to sphinx events."""
    app.connect("autodoc-process-docstring", remove_module_docstring)

    app.add_config_value("RELEASE_LEVEL", "", "env")
