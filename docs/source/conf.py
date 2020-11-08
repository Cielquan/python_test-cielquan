# noqa: D205,D208,D400
"""
    docs.source.conf
    ~~~~~~~~~~~~~~~~

    Configuration file for the Sphinx documentation builder.

    :copyright: 2020 (c) Christian Riedel
    :license: MIT, see LICENSE.rst for more details
"""
# pylint: disable=invalid-name
import os
import re
import sys

from datetime import date
from importlib.util import find_spec
from pathlib import Path
from typing import Any, List, Union

import sphinx_rtd_theme  # type: ignore[import]

from dotenv import find_dotenv, load_dotenv
from formelsammlung.envvar import getenv_typed
from sphinx.application import Sphinx

from python_test_cielquan import (
    __author__,
    __gh_repository_link__,
    __project__,
    __version__,
)


needs_sphinx = "3.1"  #: Minimum Sphinx version to build the docs
sys.path.insert(0, str(Path(__file__).parents[2]))  #: Add Repo to PATH


#: -- GLOB VARS ------------------------------------------------------------------------
CONF_DIR = Path(__file__)
NOT_LOADED_MSGS = []
YEAR = f"{date.today().year}"


#: -- GLOB TYPES -----------------------------------------------------------------------
EnvVarTypes = Union[str, int, float, bool, None]


#: -- UTILS ----------------------------------------------------------------------------
load_dotenv(find_dotenv())  #: Load .env file from project root


#: -- PROJECT INFORMATION --------------------------------------------------------------
project = __project__.replace("-", "_")
author = __author__
RELEASE_YEAR = "2019"  # CHANGE ME
copyright = (  # pylint: disable=W0622  # noqa: A001,VNE003
    f"{RELEASE_YEAR}{('-' + YEAR) if YEAR != RELEASE_YEAR else ''}, " + author
)
release = __version__  #: The full version, including alpha/beta/rc tags
version_parts = re.search(
    r"^[v]?(?P<version>\d+\.\d+)\.\d+[+-]?(?P<tag>[a-zA-Z]*)\d*", __version__
)
version = (
    None if not version_parts else version_parts.group("version")
)  #: Major + Minor version like (X.Y)
RELEASE_LEVEL = (
    None if not version_parts else version_parts.group("tag")
)  #: only tags like alpha/beta/rc


#: -- GENERAL CONFIG -------------------------------------------------------------------
extensions: List[str] = []
today_fmt = "%Y-%m-%d"
exclude_patterns: List[str] = []  #: Files to exclude for source of doc

#: Added dirs for static and template files if they exist
html_static_path = ["_static"] if Path(CONF_DIR, "_static").exists() else []
templates_path = ["_templates"] if Path(CONF_DIR, "_templates").exists() else []

rst_prolog = """
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
    "issue": (f"{__gh_repository_link__}/issues/%s", "#"),
    "pull": (f"{__gh_repository_link__}/pull/%s", "pr"),
    "user": ("https://github.com/%s", "@"),
    "jira_issue": (f"{getenv_typed('JIRA_LINK')}%s", ""),
}


#: -- APIDOC ---------------------------------------------------------------------------
if find_spec("sphinxcontrib.apidoc") is not None:
    extensions.append("sphinxcontrib.apidoc")
else:
    NOT_LOADED_MSGS.append(
        "## 'sphinxcontrib-apidoc' extension not loaded - not installed"
    )
apidoc_separate_modules = True
apidoc_module_first = True
apidoc_module_dir = f"../../src/{project}"
apidoc_output_dir = "autoapi"


#: -- AUTODOC --------------------------------------------------------------------------
extensions.append("sphinx.ext.autodoc")
autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_mock_imports: List[str] = []
autodoc_default_options = {"members": True}

if find_spec("sphinx_autodoc_typehints") is not None:
    extensions.append("sphinx_autodoc_typehints")
else:
    NOT_LOADED_MSGS.append(
        "## 'sphinx-autodoc-typehints' extension not loaded - not installed"
    )


def remove_module_docstring(  # pylint: disable=R0913,W0613
    app, what, name, obj, options, lines  # noqa: ANN001
) -> None:
    """Remove module docstring."""
    if what == "module":
        del lines[:]


#: -- CLICK ----------------------------------------------------------------------------
if find_spec("sphinx_click") is not None and find_spec("click") is not None:
    extensions.append("sphinx_click.ext")
else:
    NOT_LOADED_MSGS.append(
        "## 'sphinx-click' extension not loaded - extension or 'click' not installed"
    )


#: -- CONFLUENCE BUILDER ---------------------------------------------------------------
#: needs install: "sphinxcontrib-confluencebuilder"
if tags.has("builder_confluence"):  # type: ignore # noqa
    extensions.remove("sphinx.ext.viewcode")
    extensions.append("sphinxcontrib.confluencebuilder")
confluence_publish = True
confluence_server_url = getenv_typed("CONFLUENCE_SERVER_URL")
confluence_server_user = getenv_typed("CONFLUENCE_SERVER_USER")
confluence_server_pass = getenv_typed("CONFLUENCE_SERVER_PASS")
confluence_space_name = "SWFPTOOL"
confluence_parent_page = "SPHINXTEST"
confluence_page_hierarchy = True
confluence_prev_next_buttons_location = "bottom"
confluence_timeout = 30
confluence_purge = True


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
def setup(app: Sphinx) -> None:
    """Connect custom func to sphinx events."""
    app.connect("autodoc-process-docstring", remove_module_docstring)

    app.add_config_value("RELEASE_LEVEL", "", "env")

    if not tags.has("builder_confluence"):  # type:ignore[name-defined] # noqa
        from sphinx.directives.other import SeeAlso  # pylint: disable=C0415

        class _SeeAlso(SeeAlso):
            def run(self) -> Any:
                self.content[0] = "JIRA issue: " + f":jira_issue:`{self.content[0]}`"
                return super().run()

        app.add_directive("jira_issue", _SeeAlso)


for msg in NOT_LOADED_MSGS:
    print(msg)
