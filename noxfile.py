"""Config file for nox."""
# TODO: check why nox test let cov fail and tox test not
# maybe passenv func will help?
# TODO: run tests via nox w/o env which runs tox and writes conf + add tox.ini to .gitignore
import contextlib
import os
import re
import shutil
import subprocess  # noqa: S404
import sys

from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Set

import nox
import nox.command

from formelsammlung.venv_utils import get_venv_path, get_venv_site_packages_dir
from nox.sessions import Session as _Session
from tomlkit import parse  # type: ignore[import]


#: -- MANUAL CONFIG --------------------------------------------------------------------
#: Config  # CHANGE ME
PYTHON_TEST_VERSIONS = ["3.6", "3.7", "3.8", "3.9", "3.10", "pypy3"]
SPHINX_BUILDERS = ["html", "linkcheck", "coverage", "doctest", "confluence"]

#: nox options  # CHANGE ME
nox.options.reuse_existing_virtualenvs = True


#: -- AUTO CONFIG ----------------------------------------------------------------------
IS_WIN = sys.platform == "win32"

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

TOX_CODE_TEST_VERSION_FORMAT = (
    "{"
    + ",".join([v.replace(".", "").replace("pypy", "py") for v in PYTHON_TEST_VERSIONS])
    + "}"
)
TOX_INI_FILE = f"""[tox]
minversion = 3.15.0
isolated_build = true
skipsdist = false

[testenv:py{TOX_CODE_TEST_VERSION_FORMAT}]
description = run tests with {"{basepython}"}
passenv =
    HOME
    CI
    PYTEST_*
setenv =
    PIP_DISABLE_VERSION_CHECK = 1
    COVERAGE_FILE = {"{env:COVERAGE_FILE:{toxinidir}/.coverage_cache/.coverage.{envname}}"}
download = true
extras = testing
commands =
    pytest \\
    --basetemp={"{envtmpdir}"} \\
    --junitxml={"{toxinidir}"}/.junit_cache/junit.{"{envname}"}.xml \\
    --cov={"{envsitepackagesdir}"}/{PACKAGE_NAME} \\
    --cov-fail-under=0 \\
    --numprocesses={"{env:PYTEST_XDIST_N:auto}"} \\
    {"{posargs:tests}"}
"""


#: -- MONKEYPATCH SESSION --------------------------------------------------------------
class Session(_Session):  # noqa: R0903
    """Subclass of nox's Session class to add `poetry_install` method."""

    def __init__(self, runner: nox.sessions.SessionRunner) -> None:
        """Overwrite method to add passenv attribute."""
        super().__init__(runner)
        self.passenv: List[str] = []

    def setenv(self, env_vars: Dict[str, str]) -> None:
        """Set given envvars and add them to passenv."""
        for var in env_vars:
            self.passenv.append(var)
            self.env[var] = env_vars[var]

    def _run(
        self,
        *args: str,
        env: Mapping[str, str] = None,
        **kwargs: Any,
    ) -> Any:
        """Overwrite method to add env filter functionallity.

        Additional kwargs:
        :param filter_env: bool if env should be filtered
        :param passenv: list of envvars to not filter out
        """
        # Legacy support - run a function given.
        if callable(args[0]):
            return self._run_func(args[0], args[1:], kwargs)

        # Combine the env argument with our virtualenv's env vars.
        run_env = self.env.copy()
        if env is not None:
            run_env.update(env)

        # Filter env
        if kwargs.pop("filter_env", False):
            run_env = {
                var: run_env[var]
                for var in run_env
                if var
                in self._create_envvar_whitelist(
                    set(env or "")
                    | set(kwargs.pop("passenv", None) or "")
                    | set(self.passenv or "")
                )
            }

        # If --error-on-external-run is specified, error on external programs.
        if self._runner.global_config.error_on_external_run:
            kwargs.setdefault("external", "error")

        # Allow all external programs when running outside a sandbox.
        if not self.virtualenv.is_sandboxed:
            kwargs["external"] = True

        if args[0] in self.virtualenv.allowed_globals:
            kwargs["external"] = True

        # Run a shell command.
        return nox.command.run(args, env=run_env, paths=self.bin_paths, **kwargs)

    @staticmethod
    def _create_envvar_whitelist(whitelist: Optional[Set[str]] = None) -> Set[str]:
        """Merge ENVVAR whitelists.

        Based on ``tox.config.__init__.tox_addoption.passenv()``.
        """
        nox_whitelist = {"_"}

        tox_whitelist = {
            "CURL_CA_BUNDLE",
            "LANG",
            "LANGUAGE",
            "LD_LIBRARY_PATH",
            "PATH",
            "PIP_INDEX_URL",
            "PIP_EXTRA_INDEX_URL",
            "REQUESTS_CA_BUNDLE",
            "SSL_CERT_FILE",
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "NO_PROXY",
        }

        if IS_WIN:
            os_whitelist = {
                "SYSTEMDRIVE",  # needed for pip6
                "SYSTEMROOT",  # needed for python's crypto module
                "PATHEXT",  # needed for discovering executables
                "COMSPEC",  # needed for distutils cygwincompiler
                "TEMP",
                "TMP",
                # for `multiprocessing.cpu_count()` on Windows (prior to Python 3.4).
                "NUMBER_OF_PROCESSORS",
                "PROCESSOR_ARCHITECTURE",  # platform.machine()
                "USERPROFILE",  # needed for `os.path.expanduser()`
                "MSYSTEM",  # fixes tox#429
            }
        else:
            os_whitelist = {"TMPDIR"}

        custom_whitelist = set() if whitelist is None else whitelist

        return nox_whitelist | tox_whitelist | os_whitelist | custom_whitelist

    def poetry_install(
        self,
        extras: Optional[str] = None,
        no_dev: bool = True,
        no_root: bool = False,
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

        self.install("poetry>=1", env={"PIP_DISABLE_VERSION_CHECK": "1"})

        extra_deps = []
        if extras:
            extra_deps = ["--extras", extras]

        no_dev_flag = []
        if no_dev:
            no_dev_flag = ["--no-dev"]

        no_root_flag = []
        if no_root:
            no_root_flag = ["--no-root"]

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
@nox.session
@monkeypatch_session
def safety(session: Session) -> None:
    """Check all dependencies for known vulnerabilities."""
    session.poetry_install("poetry safety", no_root=True)

    req_file_path = Path(session.create_tmp()) / "requirements.txt"

    bin_dir = session.bin
    if bin_dir is None:
        raise FileNotFoundError("No 'bin' directory found for session venv.")

    #: Use `poetry show` to fill `requirements.txt`
    if sys.version_info[0:2] > (3, 6):
        cmd = subprocess.run(  # noqa: S603
            [str(Path(bin_dir) / "poetry"), "show"], check=True, capture_output=True
        )
    else:
        cmd = subprocess.run(  # noqa: S603
            [str(Path(bin_dir) / "poetry"), "show"], check=True, stdout=subprocess.PIPE
        )
    with open(req_file_path, "w") as req_file:
        req_file.write(
            re.sub(r"([\w-]+)[ (!)]+([\d.a-z-]+).*", r"\1==\2", cmd.stdout.decode())
        )

    session.run(
        "safety", "check", "-r", str(req_file_path), "--full-report", filter_env=True
    )


@nox.session()
@monkeypatch_session
def pre_commit(session: Session) -> None:
    """Format and check the code."""
    session.poetry_install("pre-commit testing docs poetry nox")

    show_diff = ["--show-diff-on-failure"]
    if "no_diff" in session.posargs or "nodiff" in session.posargs:
        with contextlib.suppress(ValueError):
            session.posargs.remove("no_diff")
        with contextlib.suppress(ValueError):
            session.posargs.remove("nodiff")
        show_diff = []

    hooks = session.posargs.copy()
    if not hooks:
        hooks.append("")

    session.passenv = ["SSH_AUTH_SOCK", "SKIP"]

    for hook in hooks:
        add_args = show_diff + [hook]
        session.run(
            "pre-commit",
            "run",
            "--all-files",
            "--color=always",
            *add_args,
            filter_env=True,
        )

    bin_dir = session.bin
    if bin_dir:
        print(
            "HINT: to add checks as pre-commit hook run: ",
            f'"{Path(bin_dir) / "pre-commit"} install -t pre-commit -t commit-msg".',
        )


@nox.session()
@monkeypatch_session
def package(session: Session) -> None:
    """Check sdist and wheel."""
    session.poetry_install("poetry twine", no_root=True)

    session.run("poetry", "build", "-vvv", filter_env=True)
    session.run("twine", "check", "dist/*", filter_env=True)


@nox.session(python=PYTHON_TEST_VERSIONS)
@monkeypatch_session
def code_test(session: Session) -> None:
    """Run tests with given python version."""
    session.setenv(
        {"COVERAGE_FILE": str(COV_CACHE_DIR / f".coverage.{session.python}")}
    )

    session.install(".[testing]")
    # session.poetry_install("testing", no_root=True)

    if not isinstance(
        session.virtualenv, (nox.sessions.CondaEnv, nox.sessions.VirtualEnv)
    ):
        raise AttributeError("Session venv has no attribute 'location'.")
    venv_path = session.virtualenv.location

    session.run(
        "pytest",
        f"--basetemp={Path(session.create_tmp())}",
        f"--junitxml={JUNIT_CACHE_DIR / f'junit.{session.python}.xml'}",
        f"--cov={get_venv_site_packages_dir(venv_path) / PACKAGE_NAME}",
        "--cov-fail-under=0",
        f"--numprocesses={session.env.get('PYTEST_XDIST_N') or 'auto'}",
        f"{session.posargs or 'tests'}",
        filter_env=True,
        passenv=["COVERAGE_FILE"],
    )


@nox.session()
@monkeypatch_session
def coverage(session: Session) -> None:
    """Combine coverage, create xml/html reports and report total/diff coverage.

    Diff coverage is against origin/master (or DIFF_AGAINST)
    """
    session.setenv({"COVERAGE_FILE": str(COV_CACHE_DIR / ".coverage")})

    extras = "coverage"
    if "report_only" in session.posargs or not session.posargs:
        extras += " diff-cover"

    session.poetry_install(extras, no_root=True)

    if "merge_only" in session.posargs or not session.posargs:
        session.run("coverage", "combine", filter_env=True, passenv=["COVERAGE_FILE"])
        session.run(
            "coverage",
            "xml",
            "-o",
            f"{COV_CACHE_DIR / 'coverage.xml'}",
            filter_env=True,
            passenv=["COVERAGE_FILE"],
        )
        session.run(
            "coverage",
            "html",
            "-d",
            f"{COV_CACHE_DIR / 'htmlcov'}",
            filter_env=True,
            passenv=["COVERAGE_FILE"],
        )

    if "report_only" in session.posargs or not session.posargs:
        session.run(
            "coverage",
            "report",
            "-m",
            f"--fail-under={session.env.get('MIN_COVERAGE') or 100}",
            filter_env=True,
            passenv=["COVERAGE_FILE"],
        )
        session.run(
            "diff-cover",
            f"--compare-branch={session.env.get('DIFF_AGAINST') or 'origin/master'}",
            "--ignore-staged",
            "--ignore-unstaged",
            f"--fail-under={session.env.get('MIN_DIFF_COVERAGE') or 100}",
            f"--diff-range-notation={session.env.get('DIFF_RANGE_NOTATION') or '..'}",
            f"{COV_CACHE_DIR / 'coverage.xml'}",
            filter_env=True,
            passenv=["COVERAGE_FILE"],
        )


@nox.session()
@monkeypatch_session
def docs(session: Session) -> None:
    """Build docs with sphinx."""
    extras = "docs"
    cmd = "sphinx-build"
    add_args = []

    if "autobuild" in session.posargs or "ab" in session.posargs:
        extras += " sphinx-autobuild"
        cmd = "sphinx-autobuild"
        add_args = ["--open-browser"]

    session.poetry_install(extras)

    session.run(
        cmd,
        "-b",
        "html",
        "-aE",
        "docs/source",
        "docs/build/html",
        *add_args,
        filter_env=True,
    )

    if not session.posargs:
        index_file = Path(NOXFILE_DIR) / "docs/build/html/index.html"
        print(f"DOCUMENTATION AVAILABLE UNDER: {index_file.as_uri()}")


@nox.parametrize("builder", SPHINX_BUILDERS)
@nox.session()
@monkeypatch_session
def docs_test(session: Session, builder: str) -> None:
    """Build and check docs with (see env name) sphinx builder."""
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
        filter_env=True,
    )


@nox.session(venv_backend="none")
@monkeypatch_session
def poetry_install_all_extras(session: Session) -> None:
    """Set up dev environment in current venv (w/o venv creation)."""
    extras = PYPROJECT["tool"]["poetry"].get("extras")

    if not extras:
        session.skip("No extras found to be installed")

    install_extras = ""
    for extra in extras:
        if not install_extras:
            install_extras = extra
        else:
            install_extras += f" {extra}"

    session.poetry_install(install_extras, no_dev=False)

    session.run("python", "-m", "pip", "list", "--format=columns", filter_env=True)
    print(f"PYTHON INTERPRETER LOCATION: {sys.executable}")


@nox.session(venv_backend="none")
def debug_import(session: Session) -> None:  # noqa: W0613
    """Hack for global import of `devtools.debug` (w/o venv creation)."""
    venv_path = get_venv_path()
    if venv_path is None:
        raise OSError("No calling venv could be detected.")

    with open(f"{get_venv_site_packages_dir(venv_path)}/_debug.pth", "w") as pth_file:
        pth_file.write("import devtools; __builtins__.update(debug=devtools.debug)\n")


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


@nox.session(python=PYTHON_TEST_VERSIONS)
@monkeypatch_session
def code_test_tox(session: Session) -> None:
    """Run tests with given python version via tox."""
    with open(Path("tox.ini"), "w") as tox_ini_file:
        tox_ini_file.writelines(TOX_INI_FILE)

    session.poetry_install("tox")

    session.run("tox", "-e", "py" + session.python.replace(".", "").replace("pypy", "py"))
