# pylint: skip-file
"""
    pre-commit-helper
    ~~~~~~~~~~~~~~~~~

    Collection of helper functions for pre-commit.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import re

from contextlib import suppress
from typing import List, Optional


#: Config
JIRA_PROJECT_TAG = "SWAT"  # CHANGE ME


with suppress(ModuleNotFoundError):
    from gitlint.git import GitCommit  # type: ignore[import]
    from gitlint.rules import (  # type: ignore[import]
        CommitMessageTitle,
        LineRule,
        RuleViolation,
    )

    class IssueLinkInTitle(LineRule):  # pylint: disable=R0903
        """Enforce issue links in title."""

        name = "jira-issue-in-title"
        id = "JI1"  # noqa: VNE003
        target = CommitMessageTitle

        def validate(self, line: str, _: GitCommit) -> List[Optional[RuleViolation]]:
            """Validate commit message.

            :param line: Commit message line to validate
            :param _: Whole commit object (not needed here)
            """
            if JIRA_PROJECT_TAG:
                regex = re.compile(r"^.*\(" + JIRA_PROJECT_TAG + r"[-]?\d+\)$")
            else:
                regex = re.compile(r"^.*\(#\d+\)$")
            if regex.search(line):
                return []

            if JIRA_PROJECT_TAG:
                msg = (
                    "Title does not contain a jira '{JIRA_PROJECT_TAG}'"
                    " issue link in parentheses at the end"
                )  #: noqa: FS003
            else:
                msg = "Title does not contain an issue link in parentheses at the end"
            return [RuleViolation(self.id, msg, line_nr=1)]
