"""
    noxfile
    ~~~~~~~

    Configuration file for nox.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import contextlib
import os
import re
import subprocess  # noqa: S404
import sys

from importlib.util import find_spec
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import nox
import tomlkit  # type: ignore[import]

from formelsammlung.nox_session import Session, session_w_poetry
from formelsammlung.venv_utils import get_venv_bin_dir, get_venv_path, get_venv_tmp_dir
from nox.command import CommandFailed
from nox.logger import logger as nox_logger


#: -- NOX OPTIONS ----------------------------------------------------------------------
nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "none"
nox.options.sessions = ["full_lint", "full_test_code", "full_test_docs"]


#: -- UTIL -----------------------------------------------------------------------------
OS = sys.platform
TOX_CALLS = os.getenv("_NOX_TOX_CALLS") == "true"
FORCE_COLOR = os.getenv("_NOX_FORCE_COLOR") == "true"
IN_CI = os.getenv("_NOX_IN_CI") == "true"

#: -- PATHS ----------------------------------------------------------------------------
NOXFILE_DIR = Path(__file__).parent
COV_CACHE_DIR = NOXFILE_DIR / ".coverage_cache"

#: -- CONFIG FROM PYPROJECT.TOML -------------------------------------------------------
with open(NOXFILE_DIR / "pyproject.toml") as pyproject_file:
    PYPROJECT = tomlkit.parse(pyproject_file.read())
PACKAGE_NAME = PYPROJECT["tool"]["poetry"]["name"]
SKIP_INSTALL = PYPROJECT["tool"]["_testing"]["skip_install"]
TOXENV_PYTHON_VERSIONS = PYPROJECT["tool"]["_testing"][f"toxenv_python_versions_{OS}"]
TOXENV_DOCS_BUILDERS = PYPROJECT["tool"]["_testing"]["toxenv_docs_builders"]


def poetry_require_venv(session: Session) -> bool:
    """Determine if poetry_install needs a venv to install into.

    :param session: nox session object
    """
    return isinstance(session.virtualenv, nox.sessions.PassthroughEnv) and not IN_CI


#: -- TOX CALLING DECORATOR ------------------------------------------------------------
def tox_caller(
    tox_target: Optional[str] = None, parametrized: bool = False
) -> Callable:
    """Decorate nox session functions to add option to run them via `tox`.

    :param tox_target: Optionally give the name of the tox env to call.
        Defaults to the decorated function's name.
    :param parametrized: if nox session is parametrized
    """

    def _decorator(session_func: Callable) -> Callable:
        def check_for_tox_call(session: Session, **kwargs: Dict[str, Any]) -> None:
            """Call session function or tox.

            :param session: nox session object
            :param kwargs: keyword arguments from e.g. parametrize
            """
            tox_env = session_func.__name__
            if tox_target:
                tox_env = tox_target.format(**kwargs) if parametrized else tox_target

            in_venv = False
            with contextlib.suppress(FileNotFoundError):
                in_venv = get_venv_path() is not None

            if not in_venv or "tox" in session.posargs:
                posargs = [arg for arg in session.posargs if arg != "tox"]
                session.log("Using `tox` as venv backend.")
                _tox_caller(session, tox_env, posargs)
            else:
                session_func(session=session, **kwargs)

        #: Overwrite name and docstring to imitate decorated function for nox
        check_for_tox_call.__name__ = session_func.__name__
        check_for_tox_call.__doc__ = session_func.__doc__

        return check_for_tox_call

    return _decorator


def _tox_caller(
    session: Session, tox_env: str, posargs: Optional[List[str]] = None
) -> None:
    """Call given tox env with given posargs.

    :param session: nox session object
    :param tox_env: tox env(s) to call; parameter to ``tox -e``
    :param posargs: posargs; defaults to None
    """
    if posargs is None:
        posargs = session.posargs

    #: Extract tox args
    tox_args: List[str] = []
    for arg in posargs:
        if arg.startswith("TOX_ARGS="):
            tox_args = arg[9:].split(",")
            posargs.remove(arg)
            break

    #: Extract nox args for nox called by tox
    nox_args: List[str] = []
    for arg in posargs:
        if arg.startswith("NOX_ARGS="):
            nox_args = arg[9:].split(",")
            posargs.remove(arg)
            break

    if not find_spec("tox"):
        session.poetry_install(
            "tox",
            no_root=True,
            no_dev=IN_CI,
            pip_require_venv=poetry_require_venv(session),
        )

    session.env["_TOX_SKIP_SDIST"] = str(SKIP_INSTALL)
    if FORCE_COLOR:
        #: Force color for nox when called by tox
        session.env["_TOX_FORCE_NOX_COLOR"] = "--forcecolor"
        #: Activate colorful output for tox
        session.env["PY_COLORS"] = "1"

    session.run("tox", "-e", tox_env, *tox_args, "--", *nox_args, "--", *posargs)


#: -- TEST SESSIONS --------------------------------------------------------------------
@nox.session
@session_w_poetry
@tox_caller()
def package(session: Session) -> None:
    """Check sdist and wheel."""
    if "skip_install" not in session.posargs:
        extras = "poetry twine"
        session.poetry_install(
            extras,
            no_root=True,
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")

    color = ["--ansi"] if FORCE_COLOR else []
    session.run("poetry", "build", *color, "-vvv")
    session.run("twine", "check", "--strict", "dist/*")


@nox.session
@session_w_poetry
@tox_caller(TOXENV_PYTHON_VERSIONS)
def test_code(session: Session) -> None:
    """Run tests with given python version."""
    if "skip_install" not in session.posargs:
        extras = "testing"
        session.poetry_install(
            extras,
            no_root=(TOX_CALLS or SKIP_INSTALL),
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")
        #: Remove processed posargs
        with contextlib.suppress(ValueError):
            session.posargs.remove("skip_install")

    interpreter = sys.implementation.__getattribute__("name")
    version = ".".join([str(v) for v in sys.version_info[0:2]])
    name = f"{OS}.{interpreter}{version}"
    session.env["COVERAGE_FILE"] = str(COV_CACHE_DIR / f".coverage.{name}")

    cov_source_dir = Path("no-spec-found")
    with contextlib.suppress(AttributeError, TypeError):
        cov_source_dir = Path(
            find_spec(PACKAGE_NAME).origin  # type: ignore[union-attr, arg-type]
        ).parent

    color = ["--color=yes"] if FORCE_COLOR else []
    posargs = session.posargs if session.posargs else ["tests"]

    session.run(
        "pytest",
        *color,
        f"--basetemp={get_venv_tmp_dir(get_venv_path(), create_if_missing=True)}",
        f"--junitxml={NOXFILE_DIR / '.junit_cache' / f'junit.{name}.xml'}",
        f"--cov={cov_source_dir}",
        f"--cov-fail-under={session.env.get('MIN_COVERAGE') or 100}",
        f"--numprocesses={session.env.get('PYTEST_XDIST_N') or 'auto'}",
        *posargs,
    )


def _coverage(session: Session, job: str) -> None:
    if "skip_install" not in session.posargs:
        extras = "coverage"
        if job in ("report", "all"):
            extras += " diff-cover"
        session.poetry_install(
            extras,
            no_root=True,
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")
        #: Remove processed posargs
        with contextlib.suppress(ValueError):
            session.posargs.remove("skip_install")

    session.env["COVERAGE_FILE"] = str(COV_CACHE_DIR / ".coverage")
    cov_xml_file = f"{COV_CACHE_DIR / 'coverage.xml'}"
    cov_html_dir = f"{COV_CACHE_DIR / 'htmlcov'}"

    if job in ("merge", "all"):
        session.run("coverage", "combine")
        session.run("coverage", "xml", "-o", cov_xml_file)
        session.run("coverage", "html", "-d", cov_html_dir)

    if job in ("report", "all"):
        raise_error = False
        min_cov = session.env.get("MIN_COVERAGE") or 100

        try:
            session.run("coverage", "report", "-m", f"--fail-under={min_cov}")
        except CommandFailed:
            raise_error = True

        session.run(
            "diff-cover",
            f"--compare-branch={session.env.get('DIFF_AGAINST') or 'origin/main'}",
            "--ignore-staged",
            "--ignore-unstaged",
            f"--fail-under={session.env.get('MIN_DIFF_COVERAGE') or 100}",
            f"--diff-range-notation={session.env.get('DIFF_RANGE_NOTATION') or '..'}",
            cov_xml_file,
        )

        if raise_error:
            raise CommandFailed


@nox.session
@session_w_poetry
@tox_caller()
def coverage_merge(session: Session) -> None:
    """Combine coverage data and create xml/html reports."""
    _coverage(session, "merge")


@nox.session
@session_w_poetry
@tox_caller()
def coverage_report(session: Session) -> None:
    """Report total and diff coverage against origin/main (or DIFF_AGAINST)."""
    _coverage(session, "report")


@nox.session
@session_w_poetry
@tox_caller()
def coverage(session: Session) -> None:
    """Run `coverage_merge` + `coverage_report`."""
    _coverage(session, "all")


@nox.session
@session_w_poetry
@tox_caller()
def safety(session: Session) -> None:
    """Check all dependencies for known vulnerabilities."""
    if "skip_install" not in session.posargs:
        extras = "poetry safety"
        session.poetry_install(
            extras,
            no_root=True,
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")

    venv_path = get_venv_path()
    req_file_path = (
        get_venv_tmp_dir(venv_path, create_if_missing=True) / "requirements.txt"
    )

    #: Use `poetry show` to fill `requirements.txt`
    command = [str(get_venv_bin_dir(venv_path) / "poetry"), "show"]
    # TODO:#i# simplify when py36 is not longer supported.
    if sys.version_info[0:2] > (3, 6):
        cmd = subprocess.run(command, check=True, capture_output=True)  # noqa: S603
    else:
        cmd = subprocess.run(command, check=True, stdout=subprocess.PIPE)  # noqa: S603
    with open(req_file_path, "w") as req_file:
        req_file.write(
            re.sub(r"([\w-]+)[ (!)]+([\d.a-z-]+).*", r"\1==\2", cmd.stdout.decode())
        )

    session.run("safety", "check", "-r", str(req_file_path), "--full-report")


@nox.session
@session_w_poetry
@tox_caller()
def pre_commit(session: Session) -> None:  # noqa: R0912
    """Format and check the code."""
    if "skip_install" not in session.posargs:
        extras = "pre-commit testing docs poetry dev_nox"
        session.poetry_install(
            extras,
            no_root=(TOX_CALLS or SKIP_INSTALL),
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")

    #: Set 'show-diff' and 'skip identity hook'
    show_diff = []
    env = {"SKIP": "identity"}
    if (session.interactive and "diff" in session.posargs) or (
        not session.interactive and "nodiff" not in session.posargs
    ):
        show_diff = ["--show-diff-on-failure"]
        env = {}

    #: Add SKIP from posargs to env
    skip = ""
    for arg in session.posargs:
        if arg.startswith("SKIP="):
            skip = arg
            break

    if skip:
        env = {"SKIP": f"{skip[5:]},{env.get('SKIP', '')}"}

    #: Get hooks from posargs
    hooks_arg = ""
    for arg in session.posargs:
        if arg.startswith("HOOKS="):
            hooks_arg = arg
            break

    #: Remove processed posargs
    for arg in ("skip_install", "diff", "nodiff", skip, hooks_arg):
        with contextlib.suppress(ValueError):
            session.posargs.remove(arg)

    hooks = hooks_arg[6:].split(",") if hooks_arg else [""]

    color = ["--color=always"] if FORCE_COLOR else []

    error_hooks = []
    for hook in hooks:
        add_args = show_diff + session.posargs + ([hook] if hook else [])
        try:
            session.run("pre-commit", "run", *color, "--all-files", *add_args, env=env)
        except CommandFailed:
            error_hooks.append(hook)

    print(
        "HINT: to add checks as pre-commit hook run: ",
        f'"{get_venv_bin_dir(get_venv_path()) / "pre-commit"} '
        "install -t pre-commit -t commit-msg.",
    )

    if error_hooks:
        if hooks != [""]:
            nox_logger.error(
                f"The following pre-commit hooks failed: {error_hooks}."  # noqa: G004
            )
        raise CommandFailed


@nox.session
@session_w_poetry
@tox_caller()
def docs(session: Session) -> None:
    """Build docs with sphinx."""
    extras = "docs"
    cmd = "sphinx-build"
    args = ["-b", "html", "-aE", "docs/source", "docs/build/html"]

    if "autobuild" in session.posargs or "ab" in session.posargs:
        extras += " sphinx-autobuild"
        cmd = "sphinx-autobuild"
        args += ["--open-browser"]

    if "skip_install" not in session.posargs:
        session.poetry_install(
            extras,
            no_root=(TOX_CALLS or SKIP_INSTALL),
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")

    #: Remove processed posargs
    for arg in ("skip_install", "autobuild", "ab"):
        with contextlib.suppress(ValueError):
            session.posargs.remove(arg)

    color = ["--color"] if FORCE_COLOR else []

    session.run(cmd, *color, *args, *session.posargs)

    index_file = NOXFILE_DIR / "docs/build/html/index.html"
    print(f"DOCUMENTATION AVAILABLE UNDER: {index_file.as_uri()}")


@nox.parametrize("builder", TOXENV_DOCS_BUILDERS[11:-1].split(","))
@nox.session
@session_w_poetry
@tox_caller("test_docs-{builder}", parametrized=True)
def test_docs(session: Session, builder: str) -> None:
    """Build and check docs with (see env name) sphinx builder."""
    if "skip_install" not in session.posargs:
        extras = "docs"
        session.poetry_install(
            extras,
            no_root=(TOX_CALLS or SKIP_INSTALL),
            no_dev=(TOX_CALLS or IN_CI),
            pip_require_venv=poetry_require_venv(session),
        )
    else:
        session.log("Skipping install step.")
        #: Remove processed posargs
        with contextlib.suppress(ValueError):
            session.posargs.remove("skip_install")

    source_dir = "docs/source"
    target_dir = f"docs/build/test/{builder}"
    std_args = ["-aE", "-v", "-nW", "--keep-going", source_dir, target_dir]

    color = ["--color"] if FORCE_COLOR else []

    session.run("sphinx-build", "-b", builder, *color, *std_args, *session.posargs)


#: -- DEV NOX SESSIONS -----------------------------------------------------------------
@nox.session
@session_w_poetry
def install_extras(session: Session) -> None:
    """Install all specified extras."""
    extras = PYPROJECT["tool"]["poetry"].get("extras")

    if not extras:
        session.skip("No extras found to be installed.")

    extras_to_install = ""
    for extra in extras:
        extras_to_install += f" {extra}"

    session.poetry_install(
        extras_to_install.strip(),
        no_root=True,
        no_dev=False,
        pip_require_venv=poetry_require_venv(session),
    )
    session.run("python", "-m", "pip", "list", "--format=columns")
    print(f"PYTHON INTERPRETER LOCATION: {sys.executable}")


@nox.session
@session_w_poetry
def setup_pre_commit(session: Session) -> None:
    """Set up pre-commit.

    (Re)Create pre-commit tox env, install pre-commit hook, run tox env.
    """
    _tox_caller(session, "pre_commit", ["TOX_ARGS=-r,--notest"])
    session.run("pre-commit", "install", "-t", "pre-commit", "-t", "commit-msg")
    _tox_caller(session, "pre_commit", [])


@nox.session
def create_spellignore(session: Session) -> None:  # noqa: W0613
    """Create .spellignore file (no overwrite)."""
    gitignore_file_path = NOXFILE_DIR / ".gitignore"
    with open(gitignore_file_path) as gitignore_file:
        gitignore_content = gitignore_file.read()

    spellignore_file_path = NOXFILE_DIR / ".spellignore"
    if not spellignore_file_path.is_file():
        with open(spellignore_file_path, "w") as spellignore_file:
            spellignore_file.writelines(gitignore_content)


@nox.session
def dev(session: Session) -> None:
    """Call basic dev setup nox sessions."""
    session.run(
        "nox", "--session", "install_extras", "setup_pre_commit", "create_spellignore"
    )


#: -- TOX MULTI WRAPPER SESSIONS -------------------------------------------------------
@nox.session
@session_w_poetry
def full_lint(session: Session) -> None:
    """Call tox to run all lint tests."""
    _tox_caller(session, "safety,pre_commit")


@nox.session
@session_w_poetry
def full_test_code(session: Session) -> None:
    """Call tox to run all code tests incl. package and coverage."""
    _tox_caller(session, f"package,{TOXENV_PYTHON_VERSIONS},coverage")


@nox.session
@session_w_poetry
def full_test_docs(session: Session) -> None:
    """Call tox to run all docs tests."""
    _tox_caller(session, TOXENV_DOCS_BUILDERS)
