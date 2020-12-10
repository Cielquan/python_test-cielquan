"""Config file for nox."""
# FIXME: try to reduce install statements
# FIXME: py310 poetry needs crashtest, but why fail?
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

from formelsammlung.venv_utils import (
    get_venv_bin_dir,
    get_venv_path,
    get_venv_site_packages_dir,
    get_venv_tmp_dir,
)
from nox.command import CommandFailed
from nox.logger import logger as nox_logger
from nox.sessions import Session as _Session


#: -- NOX OPTIONS ----------------------------------------------------------------------
nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "none"
nox.options.sessions = ["tox_lint", "tox_code", "tox_docs"]

#: -- UTIL -----------------------------------------------------------------------------
TOX_CALLS = os.getenv("_NOX_TOX_CALLS") == "true"
FORCE_COLOR = os.getenv("_NOX_FORCE_COLOR") == "true"
IN_CI = os.getenv("_NOX_IN_CI") == "true"
IN_VENV = False
with contextlib.suppress(FileNotFoundError):
    IN_VENV = get_venv_path() is not None

#: -- PATHS ----------------------------------------------------------------------------
NOXFILE_DIR = Path(__file__).parent
COV_CACHE_DIR = NOXFILE_DIR / ".coverage_cache"
JUNIT_CACHE_DIR = NOXFILE_DIR / ".junit_cache"

#: -- CONFIG FROM PYPROJECT.TOML -------------------------------------------------------
with open(NOXFILE_DIR / "pyproject.toml") as pyproject_file:
    PYPROJECT = tomlkit.parse(pyproject_file.read())
PACKAGE_NAME = PYPROJECT["tool"]["poetry"]["name"]
TOX_SKIP_SDIST = PYPROJECT["tool"]["_testing"]["tox_skip_sdist"]
TOXENV_PYTHON_VERSIONS = PYPROJECT["tool"]["_testing"]["toxenv_python_versions"]
TOXENV_DOCS_BUILDERS = PYPROJECT["tool"]["_testing"]["toxenv_docs_builders"]


#: -- MONKEYPATCH SESSION --------------------------------------------------------------
class Session(_Session):  # noqa: R0903
    """Subclass of nox's Session class to add `poetry_install` method."""

    def poetry_install(
        self,
        extras: Optional[str] = None,
        no_dev: bool = False,
        no_root: bool = False,
        require_venv: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        """Wrap ``poetry install`` for nox sessions.

        :param extras: string of space separated extras to install
        :param no_dev: if `--no-dev` should be set; defaults to: True
        :param no_root: if `--no-root` should be set; defaults to: False
        :param require_venv: If ``True`` requires to be run in a venv. If ``False`` does
            not require a venv to be run inside. If unset autodetection is used: if no
            venv is active abort install except when inside CI.
        """
        #: Safety hurdle copied from nox.sessions.Session.install()
        if not isinstance(
            self._runner.venv,
            (
                nox.sessions.CondaEnv,
                nox.sessions.VirtualEnv,
                nox.sessions.PassthroughEnv,
            ),
        ):
            raise ValueError("A session w/o a virtualenv can not install dependencies.")

        env = {"PIP_DISABLE_VERSION_CHECK": "1"}
        req_venv = {"PIP_REQUIRE_VIRTUALENV": "true"}

        if require_venv is True or (
            isinstance(self.virtualenv, nox.sessions.PassthroughEnv)
            and not IN_CI
            and require_venv is not False
        ):
            env.update(req_venv)
            if "env" in kwargs:
                kwargs["env"].update(req_venv)
            else:
                kwargs["env"] = req_venv

        self.install("poetry>=1", env=env)

        extra_deps = ["--extras", extras] if extras else []
        no_dev_flag = ["--no-dev"] if no_dev else []
        no_root_flag = ["--no-root"] if no_root else []
        install_args = no_root_flag + no_dev_flag + extra_deps
        color = ["--ansi"] if FORCE_COLOR else []

        self._run("poetry", "install", *color, *install_args, **kwargs)


def monkeypatch_session(session_func: Callable) -> Callable:
    """Decorate nox session functions to add `poetry_install` method.

    :param session_func: decorated function with commands for nox session
    """

    def switch_session_class(session: Session, **kwargs: Dict[str, Any]) -> None:
        """Call session function with session object overwritten by custom one.

        :param session: nox session object
        :param kwargs: keyword arguments from e.g. parametrize
        """
        session = Session(session._runner)  # noqa: W0212
        session_func(session=session, **kwargs)

    #: Overwrite name and docstring to imitate decorated function for nox
    switch_session_class.__name__ = session_func.__name__
    switch_session_class.__doc__ = session_func.__doc__

    return switch_session_class


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

            if not IN_VENV or "tox" in session.posargs:
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
    if posargs is None:
        posargs = session.posargs
    session.poetry_install("tox", no_root=True, no_dev=IN_CI)
    session.env["_TOX_SKIP_SDIST"] = str(TOX_SKIP_SDIST)
    if FORCE_COLOR:
        #: Force color for nox when called by tox
        session.env["_TOX_FORCE_NOX_COLOR"] = "--forcecolor"
        #: Activate colorful output for tox
        session.env["PY_COLORS"] = "1"
    session.run("tox", "-e", tox_env, *posargs)


#: -- TEST SESSIONS --------------------------------------------------------------------
@nox.session
@monkeypatch_session
@tox_caller()
def package(session: Session) -> None:
    """Check sdist and wheel."""
    if "skip_install" not in session.posargs:
        extras = "poetry twine"
        session.poetry_install(extras, no_root=True, no_dev=(TOX_CALLS or IN_CI))
    else:
        session.log("Skipping install step.")

    color = ["--ansi"] if FORCE_COLOR else []
    session.run("poetry", "build", *color, "-vvv")
    session.run("twine", "check", "dist/*")


@nox.session
@monkeypatch_session
@tox_caller(TOXENV_PYTHON_VERSIONS)
def test_code(session: Session) -> None:
    """Run tests with given python version."""
    if "skip_install" not in session.posargs:
        extras = "testing"
        session.poetry_install(extras, no_root=TOX_CALLS, no_dev=(TOX_CALLS or IN_CI))
    else:
        session.log("Skipping install step.")
        #: Remove processed posargs
        with contextlib.suppress(ValueError):
            session.posargs.remove("skip_install")

    interpreter = sys.implementation.__getattribute__("name")
    version = ".".join([str(v) for v in sys.version_info[0:2]])
    name = f"{interpreter}{version}"
    session.env["COVERAGE_FILE"] = str(COV_CACHE_DIR / f".coverage.{name}")

    cov_source_dir = Path("no-spec-found")
    with contextlib.suppress(AttributeError, TypeError):
        cov_source_dir = Path(
            find_spec(PACKAGE_NAME).origin  # type: ignore[union-attr, arg-type]
        ).parent

    color = ["--color=yes"] if FORCE_COLOR else []

    session.run(
        "pytest",
        *color,
        f"--basetemp={get_venv_tmp_dir(get_venv_path())}",
        f"--junitxml={JUNIT_CACHE_DIR / f'junit.{session.python}.xml'}",
        f"--cov={cov_source_dir}",
        f"--cov-fail-under={session.env.get('MIN_COVERAGE') or 100}",
        f"--numprocesses={session.env.get('PYTEST_XDIST_N') or 'auto'}",
        f"{session.posargs or 'tests'}",
    )


def _coverage(session: Session, job: str) -> None:
    if "skip_install" not in session.posargs:
        extras = "coverage"
        if job in ("report", "all"):
            extras += " diff-cover"
        session.poetry_install(extras, no_root=True, no_dev=(TOX_CALLS or IN_CI))
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
            f"--compare-branch={session.env.get('DIFF_AGAINST') or 'origin/master'}",
            "--ignore-staged",
            "--ignore-unstaged",
            f"--fail-under={session.env.get('MIN_DIFF_COVERAGE') or 100}",
            f"--diff-range-notation={session.env.get('DIFF_RANGE_NOTATION') or '..'}",
            cov_xml_file,
        )

        if raise_error:
            raise CommandFailed


@nox.session
@monkeypatch_session
@tox_caller()
def coverage_merge(session: Session) -> None:
    """Combine coverage data and create xml/html reports."""
    _coverage(session, "merge")


@nox.session
@monkeypatch_session
@tox_caller()
def coverage_report(session: Session) -> None:
    """Report total and diff coverage against origin/master (or DIFF_AGAINST)."""
    _coverage(session, "report")


@nox.session
@monkeypatch_session
@tox_caller()
def coverage(session: Session) -> None:
    """Run `coverage_merge` + `coverage_report`."""
    _coverage(session, "all")


@nox.session
@monkeypatch_session
@tox_caller()
def safety(session: Session) -> None:
    """Check all dependencies for known vulnerabilities."""
    if "skip_install" not in session.posargs:
        extras = "poetry safety"
        session.poetry_install(extras, no_root=True, no_dev=(TOX_CALLS or IN_CI))
    else:
        session.log("Skipping install step.")

    venv_path = get_venv_path()
    req_file_path = get_venv_tmp_dir(venv_path) / "requirements.txt"

    #: Use `poetry show` to fill `requirements.txt`
    command = [str(get_venv_bin_dir(venv_path) / "poetry"), "show"]
    # TODO: simplify when py36 is not longer supported.  # noqa: W0511
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
@monkeypatch_session
@tox_caller()
def pre_commit(session: Session) -> None:  # noqa: R0912
    """Format and check the code."""
    if "skip_install" not in session.posargs:
        extras = "pre-commit testing docs poetry nox"
        session.poetry_install(extras, no_root=TOX_CALLS, no_dev=(TOX_CALLS or IN_CI))
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
            nox_logger.error(f"The following pre-commit hooks failed: {error_hooks}.")
        raise CommandFailed


@nox.session
@monkeypatch_session
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
        session.poetry_install(extras, no_root=TOX_CALLS, no_dev=(TOX_CALLS or IN_CI))
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
@monkeypatch_session
@tox_caller("test_docs-{builder}", parametrized=True)
def test_docs(session: Session, builder: str) -> None:
    """Build and check docs with (see env name) sphinx builder."""
    if "skip_install" not in session.posargs:
        extras = "docs"
        session.poetry_install(extras, no_root=TOX_CALLS, no_dev=(TOX_CALLS or IN_CI))
    else:
        session.log("Skipping install step.")
        #: Remove processed posargs
        with contextlib.suppress(ValueError):
            session.posargs.remove("skip_install")

    source_dir = "docs/source"
    target_dir = f"docs/build/test/{builder}"
    std_args = ["-aE", "-v", "-nW", "--keep-going", source_dir, target_dir]
    add_args = ["-t", "builder_confluence"] if builder == "confluence" else []

    color = ["--color"] if FORCE_COLOR else []

    session.run(
        "sphinx-build", "-b", builder, *color, *std_args, *add_args, *session.posargs
    )


#: -- DEV NOX SESSIONS -----------------------------------------------------------------
@nox.session
@monkeypatch_session
def install_extras(session: Session) -> None:
    """Install all specified extras."""
    extras = PYPROJECT["tool"]["poetry"].get("extras")

    if not extras:
        session.skip("No extras found to be installed.")

    extras_to_install = ""
    for extra in extras:
        extras_to_install += f" {extra}"

    session.poetry_install(extras_to_install.strip(), no_dev=False)
    session.run("python", "-m", "pip", "list", "--format=columns")
    print(f"PYTHON INTERPRETER LOCATION: {sys.executable}")


@nox.session
def setup_pre_commit(session: Session) -> None:
    """Set up pre-commit.

    (Re)Create pre-commit tox env, install pre-commit hook, run tox env.
    """
    _tox_caller(session, "pre_commit", ["-r", "--notest"])
    session.run("pre-commit", "install", "-t", "pre-commit", "-t", "commit-msg")
    _tox_caller(session, "pre_commit", [])


DEBUG_PY_FILE = """# Import devtools if installed and add to builtins
from importlib.util import find_spec
if find_spec('devtools'):
    import devtools
    __builtins__.update(debug=devtools.debug)
"""


@nox.session
def debug_import(session: Session) -> None:  # noqa: W0613
    """Hack for global import of `devtools.debug` in active venv."""
    file_path = get_venv_site_packages_dir(get_venv_path())
    filename = "__devtools_debug_import_hack"

    with open(f"{file_path / f'{filename}.pth'}", "w") as pth_file:
        pth_file.write(f"import {filename}\n")

    with open(f"{file_path / f'{filename}.py'}", "w") as py_file:
        py_file.writelines(DEBUG_PY_FILE)


PDBRC_FILE = """# .pdbrc file generated by nox
import IPython
from traitlets.config import get_config

cfg = get_config()
cfg.InteractiveShellEmbed.colors = "Linux"
cfg.InteractiveShellEmbed.confirm_exit = False

# Use IPython for interact
alias interacti IPython.embed(config=cfg)

# Print a dictionary, sorted. %1 is the dict, %2 is the prefix for the names
alias p_ for k in sorted(%1.keys()): print("%s%-15s= %-80.80s" % ("%2",k,repr(%1[k]))

# Print member vars of a thing
alias pi p_ %1.__dict__ %1.

# Print member vars of self
alias ps pi self

# Print locals
alias pl p_ locals() local:

# Next and list
alias nl n;;l

# Step and list
alias sl s;;l
"""


@nox.session
def pdbrc(session: Session) -> None:  # noqa: W0613
    """Create .pdbrc file (no overwrite)."""
    pdbrc_file_path = NOXFILE_DIR / ".pdbrc"
    if not pdbrc_file_path.is_file():
        with open(pdbrc_file_path, "w") as pdbrc_file:
            pdbrc_file.writelines(PDBRC_FILE)


#: -- TOX MULTI WRAPPER SESSIONS -------------------------------------------------------
@nox.session
@monkeypatch_session
def tox_lint(session: Session) -> None:
    """Call tox to run all lint tests."""
    _tox_caller(session, "safety,pre_commit")


@nox.session
@monkeypatch_session
def tox_code(session: Session) -> None:
    """Call tox to run all code tests incl. package and coverage."""
    _tox_caller(session, f"package,{TOXENV_PYTHON_VERSIONS},coverage")


@nox.session
@monkeypatch_session
def tox_docs(session: Session) -> None:
    """Call tox to run all docs tests."""
    _tox_caller(session, TOXENV_DOCS_BUILDERS)
