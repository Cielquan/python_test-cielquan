"""Script to call executables in `tox` envs.

The script takes two mandatory arguments:
1. the executable to call like e.g. `pylint`
2. a string with comma separated `tox` envs to check for the executable

All other arguments after are passed to the tool on call.

The script considers OS and calls the tool accordingly.
"""
import re
import subprocess  # nosec
import sys

from contextlib import suppress
from pathlib import Path
from typing import List, Optional


with suppress(ModuleNotFoundError):
    from gitlint.rules import (  # type: ignore[import]
        CommitMessageTitle,
        LineRule,
        RuleViolation,
    )

    JIRA_ISSUE_TAG = ""  # CHANGE ME

    class JiraIssueInTitle(LineRule):
        """Enforce jira issue tag in title."""

        name = "jira-issue-in-title"
        id = "JI1"
        target = CommitMessageTitle

        def validate(self, line, commit) -> List[Optional[RuleViolation]]:
            """Validate commit message."""
            if JIRA_ISSUE_TAG:
                regex = re.compile(r"^.*\(" + JIRA_ISSUE_TAG + r"[-]?\d+\)$")
            else:
                regex = re.compile(r"^.*\(#\d+\)$")
            if regex.search(line):
                return []

            msg = "Title does not contain an 'issue tag' in paratheses at the end"
            return [RuleViolation(self.id, msg, line_nr=1)]


def tox_env_exe_runner() -> int:
    """Call given `tool` from given `tox` env."""
    tool = sys.argv[1]

    if sys.platform == "win32":
        exe = Path("Scripts/" + tool + ".exe")
    else:
        exe = Path("bin/" + tool)

    tox = Path(".tox")
    envs = sys.argv[2].split(",")

    cmd = None
    for env in envs:
        path = Path(tox / env / exe)
        if path.is_file():
            cmd = (str(path), *sys.argv[3:])

    if cmd is None:
        print(
            f"No '{tool}' executable found. Make sure one of the "
            f"following `tox` envs is accessible: {envs}"
        )
        return 1

    return subprocess.call(cmd)  # nosec


if __name__ == "__main__":
    sys.exit(tox_env_exe_runner())
