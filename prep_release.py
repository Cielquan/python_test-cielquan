"""
    prep_release
    ~~~~~~~~~~~~

    Script for preparing the repo for a new release.

    1) Bump version
    2) Finish CHANGELOG.md
    3) git commit and tag

    :copyright: (c) 2019-2020, Christian Riedel
    :license: GPL-3.0, see LICENSE for details
"""  # noqa: D205,D208,D400
import argparse
import re
import subprocess  # noqa: S404
import sys

from datetime import date

import tomlkit  # type: ignore[import]


if sys.version_info[0:2] <= (3, 6):
    raise Exception


PATCH = ("patch",)
MINOR = ("minor", "feature")
MAJOR = ("major", "breaking")


#: -- UTILS ----------------------------------------------------------------------------
def _get_pyproject_config() -> tomlkit.toml_document.TOMLDocument:
    """Load config from pyproject.toml file.

    :return: config as dict-like object
    """
    with open("pyproject.toml") as pyproject_file:
        return tomlkit.parse(pyproject_file.read())


def _set_pyproject_config(pyproject_config: tomlkit.toml_document.TOMLDocument) -> None:
    """Write given config to pyproect.toml file.

    :param pyproject_config: config to write
    """
    with open("pyproject.toml", "w") as pyproject_file:
        pyproject_file.write(tomlkit.dumps(pyproject_config))


def _get_current_version() -> str:
    """Extract the version from pyproject.toml file.

    :return: version string
    """
    return str(_get_pyproject_config()["tool"]["poetry"]["version"])


def _get_repo_url() -> str:
    """Extract source code URL at GitHub from pyproject.toml file.

    :return: URL
    """
    return str(_get_pyproject_config()["tool"]["poetry"]["urls"]["Source"])


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
        raise ValueError(f"Invalid version increase type: {release_type}")

    pyproject_config = _get_pyproject_config()
    current_version = pyproject_config["tool"]["poetry"]["version"]

    version_parts = re.match(
        r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", current_version
    )
    if not version_parts:
        raise ValueError(f"Unparsable version: {current_version}")

    if release_type in MAJOR:
        version = (
            f"{int(version_parts.group('major')) + 1}"
            f".{version_parts.group('minor')}"
            f".{version_parts.group('patch')}"
        )
    elif release_type in MINOR:
        version = (
            f"{version_parts.group('major')}"
            f".{int(version_parts.group('minor')) + 1}"
            f".{version_parts.group('patch')}"
        )
    elif release_type in PATCH:
        version = (
            f"{version_parts.group('major')}"
            f".{version_parts.group('minor')}"
            f".{int(version_parts.group('patch')) + 1}"
        )
    else:
        print("Given `RELEASE TYPE` is invalid.")
        sys.exit(1)

    pyproject_config["tool"]["poetry"]["version"] = version
    _set_pyproject_config(pyproject_config)
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
        changelog_lines[release_line] = (
            f"## Unreleased - [diff]({repo_url}/compare/v{new_version}...master)\n\n\n"
            f"## [{new_version}]({repo_url}/releases/v{new_version}) ({today})"
            f" - [diff]({repo_url}/compare/"
            f"{'' if first_release else 'v'}{last_version}...v{new_version})"
        )

    with open("CHANGELOG.md", "w") as changelog_file:
        changelog_file.write("\n".join(changelog_lines))


def commit_and_tag(version: str) -> None:
    """Git commit and tag the new release."""
    subprocess.run(  # noqa: S603,S607
        [
            "git",
            "commit",
            "--no-verify",
            f"--message='release v{version}'",
            "--include",
            "pyproject.toml",
            "CHANGELOG.md",
        ],
        check=True,
    )
    subprocess.run(  # noqa: S603,S607
        ["git", "tag", "-am", f"'v{version}'", f"v{version}"], check=True
    )


def _parser() -> argparse.Namespace:
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
    args = _parser()

    if args.first_release:
        release_version = _get_current_version()
        #: Get first commit
        current_version = subprocess.run(  # noqa: S603,S607
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            check=True,
            capture_output=True,
        ).stdout.decode()[0:7]
    else:
        release_version = bump_version(args.increase_type)
        current_version = _get_current_version()
    update_changelog(
        release_version, current_version, _get_repo_url(), args.first_release
    )
    commit_and_tag(release_version)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
