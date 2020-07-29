# noqa: D205,D208,D400
"""
    docs.source.conf
    ~~~~~~~~~~~~~~~~

    Configuration file for the Sphinx documentation builder.

    :copyright: 2020 (c) Christian Riedel
    :license: MIT, see LICENSE.rst for more details
"""
# pylint: disable=C0103
import os
import re
import sys

from datetime import date
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Iterable, List, Union

import sphinx_rtd_theme  # type: ignore[import]

from dotenv import find_dotenv, load_dotenv

from python_test import __version__


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


def get_env_var(
    var_name: str,
    default: Any = None,
    rv_type: type = str,
    *,
    raise_error_if_no_value: bool = False,
    true_bool_values: Iterable = (1, "y", "yes", "t", True),
    false_bool_values: Iterable = (0, "n", "no", "f", False),
) -> EnvVarTypes:
    """Wrap `os.getenv` to adjust the type of the values.

    :param var_name: Name of the environment variable.
    :param default: Default value if no value is found for :param var_name:.
        Default is: `None`.
    :param rv_type: Type the value of the environment variable should be changed into.
        Default is: `str`.
    :param raise_error_if_no_value: If `True` raises an `KeyError` when no value is
        found for :param var_name: and :param default: is None.
        Parameter is keyword only and defaults to: `False`.
    :param true_bool_values: Iterable of objects whose string representations are
        matched against the environment variable's value if the :param rv_type: is
        `bool`. If a match is found `True` is returned.
        Parameter is keyword only and defaults to: (1, "y", "yes", "t", True)
    :param false_bool_values: Iterable of objects whose string representations are
        matched against the environment variable's value if the :param rv_type: is
        `bool`. If a match is found `False` is returned.
        Parameter is keyword only and defaults to: (0, "n", "no", "f", False)
    """
    env_var = os.getenv(var_name, default)

    if not env_var and default is None:
        if raise_error_if_no_value:
            raise KeyError(
                f"Environment variable '{var_name}' not set or empty and no default."
            ) from None
        return None

    if isinstance(rv_type, bool):
        true_bool_values = set(true_bool_values)
        false_bool_values = set(false_bool_values)
        if str(env_var).casefold() in (str(b).casefold() for b in true_bool_values):
            return True
        if str(env_var).casefold() in (str(b).casefold() for b in false_bool_values):
            return False
        raise KeyError(
            f"Environment variable '{var_name}' has an invalid boolean value.\n"
            f"For true use any of: {true_bool_values}\n"
            f"For false use any of: {false_bool_values}"
        ) from None

    return rv_type(env_var)


def get_release_level(version_str: str) -> str:
    """Extract release tag from version string."""
    tag = re.search(r"^[v]?\d+\.\d+\.\d+[+-]?([a-zA-Z]*)\d*", version_str)
    if tag:
        return tag.group(1)
    return ""


#: -- PROJECT INFORMATION --------------------------------------------------------------
project = "python_test"  # CHANGE ME
author = "Christian Riedel"  # CHANGE ME
RELEASE_YEAR = 2019  # CHANGE ME
copyright = (  # pylint: disable=W0622  # noqa: A001,VNE003
    f"{RELEASE_YEAR}{('-' + YEAR) if YEAR != RELEASE_YEAR else ''}, " + author
)
release = __version__  #: The full version, including alpha/beta/rc tags
version = ".".join(__version__.split(".")[0:2])  #: Major + Minor version like (X.Y)
RELEASE_LEVEL = get_release_level(__version__)  #: only tags like alpha/beta/rc


#: -- GENERAL CONFIG -------------------------------------------------------------------
extensions = []
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
    "issue": ("https://github.com/Cielquan/python_test/issues/%s", "#"),  # CHANGE ME
    "pull": ("https://github.com/Cielquan/python_test/pull/%s", "pr"),  # CHANGE ME
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


def remove_module_docstring(
    app, what, name, obj, options, lines
):  # pylint: disable=R0913,W0613
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
extensions.append("sphinxcontrib.confluencebuilder")
confluence_publish = True
confluence_server_url = "https://siegwerk.atlassian.net/wiki/"
confluence_server_user = get_env_var("CONFLUENCE_SERVER_USER")
confluence_server_pass = get_env_var("CONFLUENCE_SERVER_PASS")
confluence_space_name = "SWFPTOOL"
confluence_parent_page = "SPHINXTEST"  # "SPHINXTEST"
confluence_page_hierarchy = True
confluence_prev_next_buttons_location = "bottom"
confluence_timeout = 30
confluence_purge = True
# confluence_publish_postfix = "-test-0"  # TODO: remove

if tags.has("builder_confluence"):  # type: ignore # noqa
    extensions.remove("sphinx.ext.viewcode")


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


for msg in NOT_LOADED_MSGS:
    print(msg)
