"""Config file for nox."""
# TODO: add nox env to call full test+cov on tox
# TODO: add nox env to call full doc test on tox
# TODO: tox create env and for cmd calls nox
# TODO: nox installs only if not called by tox
# TODO: nox sessions have no venv
import contextlib
import re
import subprocess  # noqa: S404
import sys

from pathlib import Path
from typing import Any, Callable, Dict, Optional

import nox
import nox.command

from formelsammlung.venv_utils import get_venv_path, get_venv_site_packages_dir
from nox.sessions import Session as _Session
from tomlkit import parse  # type: ignore[import]


#: -- MANUAL CONFIG --------------------------------------------------------------------
#: Config  # CHANGE ME
# TODO: grab from "tox -l" or "tox -a" ?
PYTHON_TEST_VERSIONS = ["3.6", "3.7", "3.8", "3.9", "3.10", "pypy3"]
SPHINX_BUILDERS = ["html", "linkcheck", "coverage", "doctest", "confluence"]

#: nox options  # CHANGE ME
nox.options.reuse_existing_virtualenvs = True


#: -- AUTO CONFIG ----------------------------------------------------------------------
IS_WIN = sys.platform == "win32"
OS_BIN = "Scripts" if IS_WIN else "bin"
#: Make sure noxfile is at repo root
NOXFILE_DIR = Path(__file__).parent
if not (NOXFILE_DIR / ".git").is_dir():
    raise FileNotFoundError(
        "No `.git` directory found. "
        f"This file '{__file__}' is not in the repository root directory."
    )

#: Load pyproject.toml
if not (NOXFILE_DIR / "pyproject.toml").is_file():
    raise FileNotFoundError("No 'pyproject.toml' file found.")
with open(NOXFILE_DIR / "pyproject.toml") as pyproject_file:
    PYPROJECT = parse(pyproject_file.read())

COV_CACHE_DIR = NOXFILE_DIR / ".coverage_cache"
JUNIT_CACHE_DIR = NOXFILE_DIR / ".junit_cache"
PACKAGE_NAME = str(PYPROJECT["tool"]["poetry"]["name"])


#: -- MONKEYPATCH SESSION --------------------------------------------------------------
class Session(_Session):  # noqa: R0903
    """Subclass of nox's Session class to add `poetry_install` method."""

    def poetry_install(
        self,
        extras: Optional[str] = None,
        no_dev: bool = False,
        no_root: bool = False,
        require_venv: bool = False,
        **kwargs: Any,
    ) -> None:
        """Wrap `poetry install` for nox sessions.

        :param extras: string of space separated extras to install
        :param no_dev: if `--no-dev` should be set; defaults to: True
        :param no_root: if `--no-root` should be set; defaults to: False
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
            raise ValueError(
                "A session without a virtualenv can not install dependencies."
            )

        _env = {"PIP_DISABLE_VERSION_CHECK": "1"}
        _req_venv = {"PIP_REQUIRE_VIRTUALENV": "true"}

        if require_venv or isinstance(self.virtualenv, nox.sessions.PassthroughEnv):
            _env.update(_req_venv)
            if "env" in kwargs:
                kwargs["env"].update(_req_venv)
            else:
                kwargs["env"] = _req_venv

        self.install("poetry>=1", env=_env)

        extra_deps = ["--extras", extras] if extras else []
        no_dev_flag = ["--no-dev"] if no_dev else []
        no_root_flag = ["--no-root"] if no_root else []

        self._run(
            "poetry", "install", *no_root_flag, *no_dev_flag, *extra_deps, **kwargs
        )


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


#: -- NOX SESSIONS ---------------------------------------------------------------------
@nox.session(venv_backend="none")
@monkeypatch_session
def safety(session: Session) -> None:
    """Check all dependencies for known vulnerabilities."""
    if "called_by_tox" not in session.posargs:
        session.poetry_install("poetry safety", no_root=True)

    venv_path = get_venv_path()
    if venv_path is None:
        raise OSError("No calling venv could be detected.")

    tmp_dir = Path(venv_path) / "tmp"
    if not tmp_dir.is_dir():
        raise FileNotFoundError("Calling venv has no 'tmp' directory.")

    bin_dir = Path(venv_path) / OS_BIN
    if not bin_dir.is_dir():
        raise FileNotFoundError(f"Calling venv has no '{OS_BIN}' directory.")

    req_file_path = tmp_dir / "requirements.txt"

    # TODO: simplify when py36 is not longer supported.  # noqa: W0511
    #: Use `poetry show` to fill `requirements.txt`
    if sys.version_info[0:2] > (3, 6):
        cmd = subprocess.run(  # noqa: S603
            [str(bin_dir / "poetry"), "show"], check=True, capture_output=True
        )
    else:
        cmd = subprocess.run(  # noqa: S603
            [str(bin_dir / "poetry"), "show"], check=True, stdout=subprocess.PIPE
        )
    with open(req_file_path, "w") as req_file:
        req_file.write(
            re.sub(r"([\w-]+)[ (!)]+([\d.a-z-]+).*", r"\1==\2", cmd.stdout.decode())
        )

    session.run("safety", "check", "-r", str(req_file_path), "--full-report")


@nox.session(venv_backend="none")
@monkeypatch_session
def pre_commit(session: Session) -> None:
    """Format and check the code."""
    if "called_by_tox" not in session.posargs:
        session.poetry_install("pre-commit testing docs poetry")

    show_diff = ["--show-diff-on-failure"]
    if "no_diff" in session.posargs or "nodiff" in session.posargs:
        show_diff = []

    #: Remove processed posargs
    for arg in ("called_by_tox", "no_diff", "nodiff"):
        with contextlib.suppress(ValueError):
            session.posargs.remove(arg)

    hooks = session.posargs.copy()
    if not hooks:
        hooks.append("")

    for hook in hooks:
        add_args = show_diff + [hook]
        session.run(
            "pre-commit",
            "run",
            "--all-files",
            "--color=always",
            *add_args,
        )

    venv_path = get_venv_path()
    if venv_path is None:
        raise OSError("No calling venv could be detected.")

    bin_dir = Path(venv_path) / OS_BIN
    if not bin_dir.is_dir():
        raise FileNotFoundError(f"Calling venv has no '{OS_BIN}' directory.")

    print(
        "HINT: to add checks as pre-commit hook run: ",
        f'"{Path(bin_dir) / "pre-commit"} install -t pre-commit -t commit-msg".',
    )


@nox.session(venv_backend="none")
@monkeypatch_session
def package(session: Session) -> None:
    """Check sdist and wheel."""
    if "called_by_tox" not in session.posargs:
        session.poetry_install("poetry twine", no_root=True)

    session.run("poetry", "build", "-vvv")
    session.run("twine", "check", "dist/*")


# @nox.session(python=PYTHON_TEST_VERSIONS)
# @nox.session(venv_backend="none")
# @monkeypatch_session
# def code_test(session: Session) -> None:
#     """Run tests with given python version."""
#     session.setenv(
#         {"COVERAGE_FILE": str(COV_CACHE_DIR / f".coverage.{session.python}")}
#     )
#
#     session.install(".[testing]")
#     # session.poetry_install("testing", no_root=True)
#
#     if not isinstance(
#         session.virtualenv, (nox.sessions.CondaEnv, nox.sessions.VirtualEnv)
#     ):
#         raise AttributeError("Session venv has no attribute 'location'.")
#     venv_path = session.virtualenv.location
#
#     session.run(
#         "pytest",
#         f"--basetemp={Path(session.create_tmp())}",
#         f"--junitxml={JUNIT_CACHE_DIR / f'junit.{session.python}.xml'}",
#         f"--cov={get_venv_site_packages_dir(venv_path) / PACKAGE_NAME}",
#         "--cov-fail-under=0",
#         f"--numprocesses={session.env.get('PYTEST_XDIST_N') or 'auto'}",
#         f"{session.posargs or 'tests'}",
#     )


# @nox.session(venv_backend="none")
# @monkeypatch_session
# def coverage(session: Session) -> None:
#     """Combine coverage, create xml/html reports and report total/diff coverage.
#
#     Diff coverage is against origin/master (or DIFF_AGAINST)
#     """
#     session.setenv({"COVERAGE_FILE": str(COV_CACHE_DIR / ".coverage")})
#
#     extras = "coverage"
#     if "report_only" in session.posargs or not session.posargs:
#         extras += " diff-cover"
#
#     session.poetry_install(extras, no_root=True)
#
#     if "merge_only" in session.posargs or not session.posargs:
#         session.run("coverage", "combine")
#         session.run(
#             "coverage",
#             "xml",
#             "-o",
#             f"{COV_CACHE_DIR / 'coverage.xml'}",
#         )
#         session.run(
#             "coverage",
#             "html",
#             "-d",
#             f"{COV_CACHE_DIR / 'htmlcov'}",
#         )
#
#     if "report_only" in session.posargs or not session.posargs:
#         session.run(
#             "coverage",
#             "report",
#             "-m",
#             f"--fail-under={session.env.get('MIN_COVERAGE') or 100}",
#         )
#         session.run(
#             "diff-cover",
#             f"--compare-branch={session.env.get('DIFF_AGAINST') or 'origin/master'}",
#             "--ignore-staged",
#             "--ignore-unstaged",
#             f"--fail-under={session.env.get('MIN_DIFF_COVERAGE') or 100}",
#             f"--diff-range-notation={session.env.get('DIFF_RANGE_NOTATION') or '..'}",
#             f"{COV_CACHE_DIR / 'coverage.xml'}",
#         )


@nox.session(venv_backend="none")
@monkeypatch_session
def docs(session: Session) -> None:
    """Build docs with sphinx."""
    extras = ""

    if "called_by_tox" not in session.posargs:
        extras += " docs"

    cmd = "sphinx-build"
    args = ["-b", "html", "-aE", "docs/source", "docs/build/html"]

    if "autobuild" in session.posargs or "ab" in session.posargs:
        extras += " sphinx-autobuild"
        cmd = "sphinx-autobuild"
        args += ["--open-browser"]

    session.poetry_install(extras.strip())

    session.run(cmd, *args)

    index_file = Path(NOXFILE_DIR) / "docs/build/html/index.html"
    print(f"DOCUMENTATION AVAILABLE UNDER: {index_file.as_uri()}")


@nox.parametrize("builder", SPHINX_BUILDERS)
@nox.session(venv_backend="none")
@monkeypatch_session
def docs_test(session: Session, builder: str) -> None:
    """Build and check docs with (see env name) sphinx builder."""
    if "called_by_tox" not in session.posargs:
        session.poetry_install("docs")

    session.run(
        "sphinx-build",
        "-b",
        builder,
        "-aE",
        "-v",
        "-nW",
        "--keep-going",
        "docs/source",
        f"docs/build/test/{builder}",
        *(["-t", "builder_confluence"] if builder == "confluence" else []),
    )


@nox.session(venv_backend="none")
@monkeypatch_session
def poetry_install_all_extras(session: Session) -> None:
    """Set up dev environment in current venv (w/o venv creation)."""
    extras = PYPROJECT["tool"]["poetry"].get("extras")

    if not extras:
        session.skip("No extras found to be installed.")

    install_extras = ""
    for extra in extras:
        if not install_extras:
            install_extras = extra
        else:
            install_extras += f" {extra}"

    session.poetry_install(install_extras, no_dev=False)

    session.run("python", "-m", "pip", "list", "--format=columns")
    print(f"PYTHON INTERPRETER LOCATION: {sys.executable}")


@nox.session(venv_backend="none")
def debug_import(session: Session) -> None:  # noqa: W0613
    """Hack for global import of `devtools.debug` (w/o venv creation)."""
    venv_path = get_venv_path()
    if venv_path is None:
        raise OSError("No calling venv could be detected.")

    with open(f"{get_venv_site_packages_dir(venv_path)}/_debug.pth", "w") as pth_file:
        pth_file.write("import _debug\n")

    with open(f"{get_venv_site_packages_dir(venv_path)}/_debug.py", "w") as py_file:
        py_file.write("from importlib.util import find_spec\n")
        py_file.write("if find_spec('devtools'):\n")
        py_file.write("    import devtools\n")
        py_file.write("    __builtins__.update(debug=devtools.debug)\n")


@nox.session(venv_backend="none")
def pdbrc(session: Session) -> None:  # noqa: W0613
    """Create .pdbrc file (w/o venv creation)."""
    pdbrc_file_path = NOXFILE_DIR / ".pdbrc"
    if not pdbrc_file_path.is_file():
        with open(pdbrc_file_path, "w") as pdbrc_file:
            pdbrc_file.write("import IPython\n")
            pdbrc_file.write("from traitlets.config import get_config\n\n")
            pdbrc_file.write("cfg = get_config()\n")
            pdbrc_file.write("""cfg.InteractiveShellEmbed.colors = "Linux"\n""")
            pdbrc_file.write("cfg.InteractiveShellEmbed.confirm_exit = False\n\n")
            pdbrc_file.write("# Use IPython for interact\n")
            pdbrc_file.write("alias interacti IPython.embed(config=cfg)\n\n")
            pdbrc_file.write(
                "# Print a dictionary, sorted. "
                + "%1 is the dict, %2 is the prefix for the names\n"
            )
            pdbrc_file.write(
                "alias p_ for k in sorted(%1.keys()): "
                + """print("%s%-15s= %-80.80s" % ("%2",k,repr(%1[k]))\n\n"""
            )
            pdbrc_file.write("# Print member vars of a thing\n")
            pdbrc_file.write("alias pi p_ %1.__dict__ %1.\n\n")
            pdbrc_file.write("# Print member vars of self\n")
            pdbrc_file.write("alias ps pi self\n\n")
            pdbrc_file.write("# Print locals\n")
            pdbrc_file.write("alias pl p_ locals() local:\n\n")
            pdbrc_file.write("# Next and list\n")
            pdbrc_file.write("alias nl n;;l\n\n")
            pdbrc_file.write("# Step and list\n")
            pdbrc_file.write("alias sl s;;l\n")
