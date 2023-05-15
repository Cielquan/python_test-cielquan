"""Script for preparing the repo for a new release.

This script needs `tomlkit` installed as dependency.

This script does:
1) Bump version
2) Finish CHANGELOG.md
3) git commit and tag

Call this for more information on usage::

    $ python prep_release.py --help

:copyright: (c) 2019-2020, Christian Riedel and AUTHORS
:license: GPL-3.0-or-later, see LICENSE for details
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date


if sys.version_info[0:2] <= (3, 6):
    msg = "Script runs only with python 3.7 or newer."
    raise RuntimeError(msg)


PATCH = ("patch", "bugfix")
MINOR = ("minor", "feature")
MAJOR = ("major", "breaking")


#: -- UTILS ----------------------------------------------------------------------------
class PyprojectError(Exception):
    """Exception for lookup errors in pyproject.toml file."""


def _get_config_value(section: str, key: str) -> str:
    """Extract a config value from pyproject.toml file.

    :return: config value
    """
    with open("pyproject.toml") as pyproject_file:
        pyproject = pyproject_file.read().split("\n")

    start = False
    for line in pyproject:
        if not start and line.strip().startswith(section):
            start = True
            continue

        if start and line.strip().startswith("["):
            break

        if start and line.strip().startswith(key):
            match = re.match(r"\s*" + key + r"""\s?=\s?["']{1}([^"']*)["']{1}.*""", line)
            if match:
                return match.group(1)
            msg = f"No value for key '{key}' in {section} section could be extracted."
            raise PyprojectError(msg)

    msg = f"No '{key}' found in {section} section."
    raise PyprojectError(msg)


def _set_config_value(section: str, key: str, value: str) -> None:
    """Set a config value in pyproject.toml file."""
    with open("pyproject.toml") as pyproject_file:
        pyproject = pyproject_file.read().split("\n")

    start = False
    for idx, line in enumerate(pyproject):
        if not start and line.strip().startswith(section):
            start = True
            continue

        if start and line.strip().startswith("["):
            msg = f"No '{key}' found in {section} section."
            raise PyprojectError(msg)

        if start and line.strip().startswith(key):
            match = re.sub(
                r"(\s*" + key + r"""\s?=\s?["']{1})[^"']*(["']{1}.*)""",
                f"\\g<1>{value}\\g<2>",
                line,
            )
            pyproject[idx] = match
            break

    with open("pyproject.toml", "w") as pyproject_file:
        pyproject_file.write("\n".join(pyproject))


#: -- MAIN -----------------------------------------------------------------------------
def bump_version(release_type: str = "patch") -> str:
    """Bump the current version for the next release.

    :param release_type: type of release;
        allowed values are: patch | minor/feature | major/breaking;
        defaults to "patch"
    :raises ValueError: when an invalid release_type is given.
    :raises ValueError: when the version string from pyproject.toml is not parsable.
    :return: new version string
    """
    if release_type not in PATCH + MINOR + MAJOR:
        msg = f"Invalid version increase type: {release_type}"
        raise ValueError(msg)

    current_version = _get_config_value("[tool.poetry]", "version")

    version_parts = re.match(r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", current_version)
    if not version_parts:
        msg = f"Unparsable version: {current_version}"
        raise ValueError(msg)

    if release_type in MAJOR:
        version = f"{int(version_parts.group('major')) + 1}.0.0"
    elif release_type in MINOR:
        version = f"{version_parts.group('major')}" f".{int(version_parts.group('minor')) + 1}.0"
    elif release_type in PATCH:
        version = (
            f"{version_parts.group('major')}"
            f".{version_parts.group('minor')}"
            f".{int(version_parts.group('patch')) + 1}"
        )
    else:
        print("Given `RELEASE TYPE` is invalid.")
        sys.exit(1)

    _set_config_value("[tool.poetry]", "version", version)
    return version


def update_changelog(
    new_version: str, last_version: str, repo_url: str, first_release: bool
) -> None:
    """Update CHANGELOG.md to be release ready.

    :param new_version: new version string
    :param last_version: current version string
    :param repo_url: URL to source code at GitHub
    :first_release: if this is the first release
    """
    with open("CHANGELOG.md") as changelog_file:
        changelog_lines = changelog_file.read().split("\n")

    release_line = 0

    for idx, line in enumerate(changelog_lines):
        if line.startswith("## Unreleased"):
            release_line = idx

    if release_line:
        today = date.today().isoformat()
        compare = f"{'' if first_release else 'v'}{last_version}...v{new_version}"
        changelog_lines[release_line] = (
            "## Unreleased\n"
            f"[diff v{new_version}...main]"
            f"({repo_url}/compare/v{new_version}...main)\n"
            "\n"
            "\n"
            f"## [{new_version}]({repo_url}/releases/v{new_version}) ({today})\n"
            f"[diff {compare}]({repo_url}/compare/{compare})"
        )

    #: Remove [diff ...] link line
    if len(changelog_lines) - 1 >= release_line + 1:
        changelog_lines.pop(release_line + 1)

    with open("CHANGELOG.md", "w") as changelog_file:
        changelog_file.write("\n".join(changelog_lines))


def commit_and_tag(version: str) -> None:
    """Git commit and tag the new release."""
    subprocess.run(
        [
            "git",
            "commit",
            "--no-verify",
            f"--message=release v{version} [skip ci]",
            "--include",
            "pyproject.toml",
            "CHANGELOG.md",
        ],
        check=True,
    )
    subprocess.run(["git", "tag", "-am", f"'v{version}'", f"v{version}"], check=True)


def _parser() -> argparse.Namespace:
    """Create parser and return parsed args."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "increase_type",
        metavar="RELEASE TYPE",
        default="patch",
        nargs="?",
        help=(
            "Release type: patch | minor/feature | major/breaking; "
            "gets ignored on `--first-release`; "
            "defaults to patch"
        ),
    )
    parser.add_argument(
        "--first-release",
        action="store_true",
        help="Flag for first release to prevent version bumping.",
    )
    return parser.parse_args()


def _main() -> int:
    """Prepare release main routine."""
    args = _parser()

    if args.first_release:
        release_version = _get_config_value("[tool.poetry]", "version")
        #: Get first commit
        current_version = subprocess.run(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            check=True,
            capture_output=True,
        ).stdout.decode()[0:7]
    else:
        current_version = _get_config_value("[tool.poetry]", "version")
        release_version = bump_version(args.increase_type)
    update_changelog(
        release_version,
        current_version,
        _get_config_value("[tool.poetry.urls]", '"Source"'),
        args.first_release,
    )
    commit_and_tag(release_version)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
