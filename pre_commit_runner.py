#!/usr/bin/env python3
"""Script to call local installations of tools from `pre-commit`.

Script considers OS and calls tool accordingly.
"""
import subprocess
import sys

from pathlib import Path


def main():
    """Call `tool` given as first argument from a tox env"""
    if sys.platform == "win32":
        exe = Path("Scripts/" + sys.argv[1] + ".exe")
    else:
        exe = Path("bin/" + sys.argv[1])

    tox = Path(".tox")
    envs = ("pre-commit", "dev", "devug")

    cmd = None
    for env in envs:
        path = Path(tox / env / exe)
        if path.is_file():
            cmd = (str(path), *sys.argv[2:])

    if cmd is None:
        print(
            "No '{}' executable found. Make sure one of the "
            "following `tox` envs is accessible: {}".format(sys.argv[1], envs)
        )
        return 1

    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
