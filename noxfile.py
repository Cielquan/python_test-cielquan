"""Config file for nox."""
# TODO: fix docstrings
import os
import re
import shutil
import subprocess  # noqa: S404
import sys

from pathlib import Path
from typing import Callable, Optional, Tuple, Union

import nox

from nox.sessions import Session as _Session
from tomlkit import parse  # type: ignore[import]


IS_WIN = sys.platform != "win32"


#: Config  # CHANGE ME
PYTHON_TEST_VERSIONS = ["3.6", "3.7", "3.8", "3.9", "3.10", "pypy3"]
SPHINX_BUILDERS = ["html", "linkcheck", "coverage", "doctest", "confluence"]

#: nox options  # CHANGE ME
nox.options.reuse_existing_virtualenvs = True


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


class Session(_Session):  # noqa: R0903
    """Subclass of nox's Session class to add `poetry_install` method."""

    def poetry_install(
        self,
        extras: Optional[str] = None,
        no_dev: bool = True,
        no_root: bool = False,
    ) -> None:
        """Wrap `poetry install` for nox envs.

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
        ):  # pragma: no cover
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

        self._run("poetry", "install", *no_root_flag, *no_dev_flag, *extra_deps)


def add_poetry_install(session_func: Callable) -> Callable:
    """Decorate nox session functions to add `poetry_install` method.

    :param session_func: decorated function with commands for nox session
    """

    def monkeypatch_install(session: Session) -> None:
        """Call session function with session object overwritten by custom one.

        :param session: nox session object
        """
        session = Session(session._runner)  # noqa: W0212
        session_func(session)

    #: Overwrite name and docstring to imitate decorated function for nox
    monkeypatch_install.__name__ = session_func.__name__
    monkeypatch_install.__doc__ = session_func.__doc__
    return monkeypatch_install


def get_calling_venv_path() -> Optional[str]:
    """Return venv path or None if no venv is used to call nox.

    :return: venv path or None
    """
    if hasattr(sys, "real_prefix"):
        return sys.real_prefix  # type: ignore[no-any-return,attr-defined] # noqa: E1101
    if sys.base_prefix != sys.prefix:
        return sys.prefix
    return None


def get_venv_site_packages_dir(venv_path: Union[str, Path]) -> Path:
    """Return path of given venv's site-packages dir.

    :param venv_path: path to venv
    :return: path to given venv's site-packages dir
    """
    return list(Path(venv_path).glob("**/site-packages"))[0]


def where_installed(program: str) -> Tuple[int, Optional[str], Optional[str]]:
    """Return exit code based on found installation places.

    Exit codes:
    0 = nowhere
    1 = venv
    2 = global
    3 = both

    :return: Exit code, venv exe, glob exe
    """
    exit_code = 0

    exe = shutil.which(program)
    if not exe:
        return exit_code, None, None

    venv_path = get_calling_venv_path()
    bin_dir = "\\Scripts" if IS_WIN else "/bin"
    path_wo_venv = os.environ["PATH"].replace(f"{venv_path}{bin_dir}", "")
    glob_exe = shutil.which(program, path=path_wo_venv)

    if venv_path and venv_path in exe:
        exit_code += 1
    else:
        exe = None
    if glob_exe:
        exit_code += 2
    return exit_code, exe, glob_exe


@nox.session
@add_poetry_install
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
            [Path(bin_dir) / "poetry", "show"], check=True, capture_output=True
        )
    else:
        cmd = subprocess.run(  # noqa: S603
            [Path(bin_dir) / "poetry", "show"], check=True, stdout=subprocess.PIPE
        )
    with open(req_file_path, "w") as req_file:
        req_file.write(
            re.sub(r"([\w-]+)[ (!)]+([\d.a-z-]+).*", r"\1==\2", cmd.stdout.decode())
        )

    session.run("safety", "check", "-r", str(req_file_path), "--full-report")


@nox.session()
@add_poetry_install
def pre_commit(session: Session) -> None:
    """Format and check the code."""
    session.poetry_install("pre-commit testing docs poetry nox")

    show_diff = ["--show-diff-on-failure"]
    if "no_diff" in session.posargs:
        session.posargs.remove("no_diff")
        show_diff = []

    if not session.posargs:
        session.posargs.append("")

    for hook in session.posargs:
        add_args = show_diff + [hook]
        session.run("pre-commit", "run", "--all-files", "--color=always", *add_args)

    bin_dir = session.bin
    if bin_dir:
        print(
            "HINT: to add checks as pre-commit hook run: ",
            f'"{Path(bin_dir) / "pre-commit"} install -t pre-commit -t commit-msg".',
        )


@nox.session()
@add_poetry_install
def package(session: Session) -> None:
    """Check sdist and wheel."""
    session.poetry_install("poetry twine", no_root=True)

    session.run("poetry", "build", "-vvv")
    session.run("twine", "check", "dist/*")


@nox.session(python=PYTHON_TEST_VERSIONS)
@add_poetry_install
def code_test(session: Session) -> None:
    """Run tests with given python version."""
    session.poetry_install("testing", no_root=False)

    session.env["COVERAGE_FILE"] = COV_CACHE_DIR / f".coverage.{session.python}"
    junit_file = JUNIT_CACHE_DIR / f"junit.{session.python}.xml"

    if not hasattr(session.virtualenv, "location"):
        raise AttributeError("Session venv has no attribute 'location'.")
    venv_path = session.virtualenv.location

    session.run(
        "pytest",
        f"--basetemp={session.create_tmp()}",
        f"--junitxml={junit_file}",
        f"--cov={get_venv_site_packages_dir(venv_path) / PACKAGE_NAME}",
        "--cov-fail-under=0",
        f"-n={session.env.get('PYTEST_XDIST_N') or 'auto'}",
        f"{session.posargs or 'tests'}",
    )


@nox.session()
@add_poetry_install
def coverage_all(session: Session) -> None:
    """Combine coverage, create xml/html reports and report total/diff coverage.

    Diff coverage is against origin/master (or DIFF_AGAINST)
    """
    extras = "coverage"
    if "report_only" in session.posargs:
        extras += "diff-cover"

    session.poetry_install(extras, no_root=True)

    session.env["COVERAGE_FILE"] = COV_CACHE_DIR / ".coverage"

    if "merge_only" in session.posargs or not session.posargs:
        session.run("coverage", "combine")
        session.run("coverage", "xml", "-o", f"{COV_CACHE_DIR/'coverage.xml'}")
        session.run("coverage", "html", "-d", f"{COV_CACHE_DIR/'htmlcov'}")

    if "report_only" in session.posargs or not session.posargs:
        session.run(
            "coverage",
            "report",
            "-m",
            f"--fail-under={session.env.get('MIN_COVERAGE') or 100}",
        )
        session.run(
            "diff-cover",
            f"--compare-branch={session.env.get('DIFF_AGAINST') or 'origin/master'}",
            "--ignore-staged",
            "--ignore-unstaged",
            f"--fail-under={session.env.get('MIN_DIFF_COVERAGE') or 100}",
            f"--diff-range-notation={session.env.get('DIFF_RANGE_NOTATION') or '..'}",
            f"{COV_CACHE_DIR/'coverage.xml'}",
        )


@nox.session()
@add_poetry_install
def docs(session: Session) -> None:
    """Build docs with sphinx."""
    session.poetry_install("docs")

    session.run("sphinx-build", "-b", "html", "-aE", "docs/source", "docs/build/html")

    index_file = Path(NOXFILE_DIR) / "docs/build/html/index.html"
    print(f"DOCUMENTATION AVAILABLE UNDER: {index_file.as_uri()}")


# TODO: fix add_poetry_install with parametrize
@nox.parametrize("builder", SPHINX_BUILDERS)
@nox.session()
@add_poetry_install
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
    )


@nox.session(venv_backend="none")
@add_poetry_install
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

    session.poetry_install(install_extras, no_root=True)

    session.run("python", "-m", "pip", "list", "--format=columns")
    print(f"PYTHON INTERPRETER LOCATION: {sys.executable}")


@nox.session(venv_backend="none")
def debug_import(session: Session) -> None:  # noqa: W0613
    """Hack for global import of `devtools.debug` (w/o venv creation)."""
    venv_path = get_calling_venv_path()
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
