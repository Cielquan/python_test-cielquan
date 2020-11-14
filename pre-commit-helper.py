# pylint: disable=invalid-name
"""
    pre-commit-helper
    ~~~~~~~~~~~~~~~~~

    Collection of helper functions for pre-commit.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import subprocess  # nosec
import sys

from pathlib import Path
from typing import List, Optional


def tox_env_exe_runner(
    tool: str, envs: List[str], tool_args: Optional[List[str]] = None
) -> int:
    """Call given `tool` from given `tox` env.

    Script to call executables in `tox` envs considering OS.

    The script takes two mandatory arguments:
    1. The executable to call like e.g. `pylint`.
    2. A string with comma separated `tox` envs to check for the executable.
        The envs are checked in given order.

    All other arguments after are passed to the tool on call.

    Returns exit code 1 if no executable is found or the exit code of the called cmd.
    """
    is_win = sys.platform == "win32"

    exe = Path(f"Scripts/{tool}.exe") if is_win else Path(f"bin/{tool}")
    cmd = None

    if not tool_args:
        tool_args = []

    for env in envs:
        path = Path(".tox") / env / exe
        if path.is_file():
            cmd = (str(path), *tool_args)

    if cmd is None:
        print(
            f"No '{tool}' executable found. Make sure one of the "
            f"following `tox` envs is accessible: {envs}"
        )
        return 1

    return subprocess.call(cmd)  # nosec


if __name__ == "__main__":
    sys.exit(tox_env_exe_runner(sys.argv[1], sys.argv[2].split(","), sys.argv[3:]))
