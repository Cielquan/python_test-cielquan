"""
    docs.source.conf
    ~~~~~~~~~~~~~~~~

    Configuration file for the Sphinx documentation builder.

    :copyright: (c) Christian Riedel
    :license: GPL-3.0, see LICENSE.txt for more details
"""  # noqa: D205,D208,D400
import os
import re

from datetime import date
from importlib.util import find_spec
from pathlib import Path
from typing import List, Optional

import sphinx_rtd_theme  # type: ignore[import]

from sphinx.application import Sphinx

from python_test_cielquan import (
    __author__,
    __gh_repository_link__,
    __project__,
    __version__,
)


needs_sphinx = "3.1"  #: Minimum Sphinx version to build the docs


#: -- GLOB VARS ------------------------------------------------------------------------
REPO_DIR = Path(__file__).parents[2]
CONF_DIR = Path(__file__)
NOT_LOADED_MSGS = []
YEAR = f"{date.today().year}"


#: -- PROJECT INFORMATION --------------------------------------------------------------
project = __project__.replace("-", "_")
author = __author__
CREATION_YEAR = 2019  # CHANGE ME
copyright = (  # noqa: VNE003
    f"{CREATION_YEAR}{('-' + YEAR) if YEAR != CREATION_YEAR else ''}, "
    + author
    + " (see :ref:`license:License` for more info)"
)
release = __version__  #: The full version, including alpha/beta/rc tags
version_parts = re.search(
    r"^v?(?P<version>\d+\.\d+)\.\d+[-.]?(?P<tag>[a-z]*)[\.]?\d*", __version__
)
#: Major + Minor version like (X.Y)
version = None if not version_parts else version_parts.group("version")
#: only tags like alpha/beta/rc
RELEASE_LEVEL = None if not version_parts else version_parts.group("tag")


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


#: -- M2R2 -----------------------------------------------------------------------------
extensions.append("m2r2")
source_suffix = [".rst", ".md"]


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
# to inspect .inv files: https://github.com/bskinn/sphobjinv
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}

extensions.append("sphinx.ext.extlinks")
extlinks = {
    "issue": (f"{__gh_repository_link__}/issues/%s", "#"),
    "pull": (f"{__gh_repository_link__}/pull/%s", "pr"),
    "user": ("https://github.com/%s", "@"),
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


def _remove_module_docstring(  # noqa: R0913
    app, what, name, obj, options, lines  # noqa: ANN001,W0613
) -> None:
    """Remove module docstring."""
    if what == "module":
        del lines[:]


#: -- SPELLING -------------------------------------------------------------------------
if find_spec("sphinxcontrib.spelling") is not None:
    extensions.append("sphinxcontrib.spelling")
else:
    NOT_LOADED_MSGS.append(
        "## 'sphinxcontrib-spelling' extension not loaded - not installed"
    )
spelling_word_list_filename = "spelling_dict.txt"
spelling_show_suggestions = True
spelling_exclude_patterns = ["autoapi/**"]


#: -- HTML THEME -----------------------------------------------------------------------
#: needs install: "sphinx-rtd-theme"
extensions.append("sphinx_rtd_theme")
html_theme = "sphinx_rtd_theme"
html_theme_options = {"style_external_links": True}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


#: -- HTML OUTPUT ----------------------------------------------------------------------
def _find_img_file(filename: str) -> Optional[str]:
    """Search for instances of given filename in sphinx config dir.

    :param filename: filename too search
    :raises FileExistsError: when more than one file with the given name exists.
    :return: None if none is found or the path as string.
    """
    img_files = list(Path(".").glob(f"{filename}.*"))
    if len(img_files) == 0:
        return None
    if len(img_files) == 1:
        return str(img_files[0])
    raise FileExistsError(
        f"Multiple '{filename}.*' files exist in the docs source dir. Please delete"
        " or rename all except one or set the appropiate file with extension in"
        " 'conf.py'."
    )


html_last_updated_fmt = today_fmt
html_show_sourcelink = True  #: Add links to *.rst source files on HTML pages
html_logo = _find_img_file("logo")
html_favicon = _find_img_file("favicon")


#: -- LaTeX OUTPUT ---------------------------------------------------------------------
latex_logo = html_logo
latex_show_pagerefs = True
latex_show_urls = "footnote"


#: -- FINAL SETUP ----------------------------------------------------------------------
def setup(app: Sphinx) -> None:
    """Connect custom func to sphinx events."""
    app.connect("autodoc-process-docstring", _remove_module_docstring)

    app.add_config_value("RELEASE_LEVEL", "", "env")


for msg in NOT_LOADED_MSGS:
    print(msg)
