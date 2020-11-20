"""Config file for nox."""
import os
import nox
import shutil
import sys
from nox.sessions import Session
from typing import Optional, Tuple
from pathlib import Path


def get_venv_path() -> Optional[str]:
    """Return venv path or None if no venv is used.

    :return: venv path or None
    """
    if hasattr(sys, "real_prefix"):
        return sys.real_prefix  # type: ignore[no-any-return,attr-defined]
    if sys.base_prefix != sys.prefix:
        return sys.prefix
    return None


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

    venv_path = get_venv_path()
    bin_dir = "\\Scripts" if sys.platform == "win32" else "/bin"
    path_wo_venv = os.environ["PATH"].replace(f"{venv_path}{bin_dir}", "")
    glob_exe = shutil.which(program, path=path_wo_venv)

    if venv_path and venv_path in exe:
        exit_code += 1
    else:
        exe = None
    if glob_exe:
        exit_code += 2
    return exit_code, exe, glob_exe


# @nox.session()
@nox.session(venv_backend="none")
def dev(session: Session) -> None:
    # TODO: grab all extras and install them
    # extras = ""
    # session.run("poetry", "install", "-E", f"{extras}")
    # f=open(r"{site_packages_dir}/_debug.pth","w");  f.write("import devtools;__builtins__.update(debug=devtools.debug)\n"); f.close()'

    # y = [path for path in sys.path]
    for path in sys.path:
        print(Path(f"{path}/lib/site-packages".casefold()))
        print(Path(path.casefold()))

    # if len(y) > 0:
    #     print("1")
    #     print(y)

    # TODO: get venv site-packages dir to add hack.pth file
    x = [path for path in sys.path if "site-packages" in path and get_venv_path() in path and "lib".casefold() in path.casefold()]
    if len(x) > 0:
        print("2")
        print(x)
    # session.run("python", "-m", "pip", "list", "--format=columns")
    # 'print("PYTHON INTERPRETER LOCATION: " + r"{venv_dir}\Scripts\python")'



# @nox.session()
# def coverage_all(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage"
#     session.install("poetry>=1")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "coverage")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "diff-cover")
#     session.run("coverage", "combine")
#     session.run(
#         "coverage",
#         "xml",
#         "-o",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/coverage.xml",
#     )
#     session.run(
#         "coverage",
#         "html",
#         "-d",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/htmlcov",
#     )
#     session.run("coverage", "report", "-m", "--fail-under=100")
#     session.run(
#         "diff-cover",
#         "--compare-branch",
#         "origin/master",
#         "--ignore-staged",
#         "--ignore-unstaged",
#         "--fail-under",
#         "100",
#         "--diff-range-notation",
#         "..",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/coverage.xml",
#     )


# @nox.session()
# def coverage_merge(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage"
#     session.install("poetry>=1")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "coverage")
#     session.run("coverage", "combine")
#     session.run(
#         "coverage",
#         "xml",
#         "-o",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/coverage.xml",
#     )
#     session.run(
#         "coverage",
#         "html",
#         "-d",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/htmlcov",
#     )


# @nox.session()
# def coverage_report(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage"
#     session.install("poetry>=1")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "coverage")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "diff-cover")
#     session.run("coverage", "report", "-m", "--fail-under=100")
#     session.run(
#         "diff-cover",
#         "--compare-branch",
#         "origin/master",
#         "--ignore-staged",
#         "--ignore-unstaged",
#         "--fail-under",
#         "100",
#         "--diff-range-notation",
#         "..",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/coverage.xml",
#     )




# @nox.session()
# def docs(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.docs"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run("sphinx-build", "-b", "html", "-aE", "docs/source", "docs/build/html")
#     session.run(
#         "python",
#         "-c",
#         'from pathlib import Path;  index_file = Path(r"C:\Users/riedelc\Projects\python_test-cielquan")/"docs/build/html/index.html"; print(f"DOCUMENTATION AVAILABLE UNDER: {index_file.as_uri()}")',
#     )


# @nox.session()
# def docs_test_confluence(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.docs-test-confluence"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run(
#         "sphinx-build",
#         "-b",
#         "confluence",
#         "-aE",
#         "-v",
#         "-nW",
#         "--keep-going",
#         "docs/source",
#         "docs/build/test/confluence",
#         "-t",
#         "builder_confluence",
#     )


# @nox.session()
# def docs_test_coverage(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.docs-test-coverage"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run(
#         "sphinx-build",
#         "-b",
#         "coverage",
#         "-aE",
#         "-v",
#         "-nW",
#         "--keep-going",
#         "docs/source",
#         "docs/build/test/coverage",
#     )


# @nox.session()
# def docs_test_doctest(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.docs-test-doctest"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run(
#         "sphinx-build",
#         "-b",
#         "doctest",
#         "-aE",
#         "-v",
#         "-nW",
#         "--keep-going",
#         "docs/source",
#         "docs/build/test/doctest",
#     )


# @nox.session()
# def docs_test_html(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.docs-test-html"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run(
#         "sphinx-build",
#         "-b",
#         "html",
#         "-aE",
#         "-v",
#         "-nW",
#         "--keep-going",
#         "docs/source",
#         "docs/build/test/html",
#     )


# @nox.session()
# def docs_test_linkcheck(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.docs-test-linkcheck"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run(
#         "sphinx-build",
#         "-b",
#         "linkcheck",
#         "-aE",
#         "-v",
#         "-nW",
#         "--keep-going",
#         "docs/source",
#         "docs/build/test/linkcheck",
#     )


# @nox.session()
# def package(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.package"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install("poetry>=1")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "poetry twine")
#     session.run("poetry", "build", "-vvv")
#     session.run("twine", "check", "dist/*")


# @nox.session()
# def pdbrc(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.pdbrc"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.run(
#         "python",
#         "-c",
#         'f=open(".pdbrc","w");  f.write("""import IPython\n""");  f.write("""from traitlets.config import get_config\n\n""");  f.write("""cfg = get_config()\n""");  f.write("""cfg.InteractiveShellEmbed.colors = "Linux"\n""");  f.write("""cfg.InteractiveShellEmbed.confirm_exit = False\n\n""");  f.write("""# Use IPython for interact\nalias interacti IPython.embed(config=cfg)\n\n""");  f.write("""# Print a dictionary, sorted. %1 is the dict, %2 is the prefix for the names\n""");  f.write("""alias p_ for k in sorted(%1.keys()): print("%s%-15s= %-80.80s" % ("%2",k,repr(%1[k]))\n\n""");  f.write("""# Print member vars of a thing\nalias pi p_ %1.__dict__ %1.\n\n""");  f.write("""# Print member vars of self\nalias ps pi self\n\n""");  f.write("""# Print locals\nalias pl p_ locals() local:\n\n""");  f.write("""# Next and list\nalias nl n;;l\n\n""");  f.write("""# Step and list\nalias sl s;;l\n"""); f.close()',
#     )


# @nox.session()
# def pre_commit(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.pre-commit"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run("pip", "install", "flake8-colors==0.1.6")
#     session.run("pre-commit", "run", "--all-files")
#     session.run(
#         "python",
#         "-c",
#         'from pathlib import Path;  exe = Path(r"C:\Users/riedelc\Projects\python_test-cielquan\.tox\pre-commit\Scripts")/"pre-commit";  print(  "HINT: to add checks as pre-commit hook run: ",  f""""{exe} install -t pre-commit -t commit-msg".""" )',
#     )


# @nox.session(python=["python3.6", "python3.7", "python3.8", "python3.9", "python3.10", "pypy3"])
# def test(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.py310"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install(".")
#     session.run(
#         "pytest",
#         R"--basetemp=C:\Users/riedelc\Projects\python_test-cielquan\.tox\py310/tmp",
#         "--cov",
#         "/python_test_cielquan",
#         "--cov-fail-under",
#         "0",
#         "--junitxml",
#         "C:/Users/riedelc/Projects/python_test-cielquan/.junit_cache/junit.py310.xml",
#         "-n=auto",
#         "tests",
#     )


# @nox.session()
# def safety(session):
#     session.env[
#         "COVERAGE_FILE"
#     ] = "C:/Users/riedelc/Projects/python_test-cielquan/.coverage_cache/.coverage.safety"
#     session.env["PIP_DISABLE_VERSION_CHECK"] = "1"
#     session.install("poetry>=1")
#     session.run("poetry", "install", "--no-root", "--no-dev", "-E", "poetry safety")
#     session.run(
#         "python",
#         "-c",
#         'f=open(r"C:\Users/riedelc\Projects\python_test-cielquan\.tox\safety/tmp/safety.py","w");  f.write("""import subprocess\n""");  f.write("""import re\n""");  f.write("""with open("C:\Users/riedelc\Projects\python_test-cielquan\.tox\safety/tmp/requirements.txt","w") as f:\n""");  f.write("""    cmd = subprocess.run(["poetry", "show"], capture_output=True)\n""");  f.write("""    cmd.check_returncode()\n""");  f.write("""    f.write(re.sub(r"([\\w-]+)[ (!)]+([\\d.a-z-]+).*", r"\\1==\\2", cmd.stdout.decode()))\n"""); f.close()',
#     )
#     session.run(
#         "python",
#         "C:/Users/riedelc/Projects/python_test-cielquan\.tox\safety/tmp/safety.py",
#     )
#     session.run(
#         "safety",
#         "check",
#         "-r",
#         "C:/Users/riedelc/Projects/python_test-cielquan\.tox\safety/tmp/requirements.txt",
#         "--full-report",
#     )
