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
import re
import subprocess  # noqa: S404

from datetime import date

import tomlkit  # type: ignore[import]


def get_pyproject_config() -> tomlkit.toml_document.TOMLDocument:
    with open("pyproject.toml") as pyproject_file:
        return tomlkit.parse(pyproject_file.read())


def set_pyproject_config(pyproject_config: tomlkit.toml_document.TOMLDocument):
    with open("pyproject.toml", "w") as pyproject_file:
        pyproject_file.write(tomlkit.dumps(pyproject_config))


def get_current_version() -> str:
    return get_pyproject_config()["tool"]["poetry"]["version"]


def get_repo_url() -> str:
    return get_pyproject_config()["tool"]["poetry"]["urls"]["Source"]


def update_changelog(new_version: str, last_version: str, repo_url: str) -> None:
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
            f" - [diff]({repo_url}/compare/v{last_version}...v{new_version})"
        )

    with open("CHANGELOG.md", "w") as changelog_file:
        changelog_file.write("\n".join(changelog_lines))


def bump_version(increase_type: str = "patch"):
    patch = tuple("patch")
    minor = ("minor", "feature")
    major = ("major", "breaking")

    if increase_type not in patch + minor + major:
        raise ValueError(f"Invalid version increase type: {increase_type}")

    pyproject_config = get_pyproject_config()
    version = pyproject_config["tool"]["poetry"]["version"]

    version_parts = re.match(r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)", version)
    if not version_parts:
        raise ValueError(f"Unparsable version: {version}")

    if increase_type in patch:
        version = (
            f"{version_parts.group('major') + 1}"
            f".{version_parts.group('minor')}"
            f".{version_parts.group('patch')}"
        )
    elif increase_type in minor:
        version = (
            f"{version_parts.group('major')}"
            f".{version_parts.group('minor') + 1}"
            f".{version_parts.group('patch')}"
        )
    elif increase_type in major:
        version = (
            f"{version_parts.group('major')}"
            f".{version_parts.group('minor')}"
            f".{version_parts.group('patch') + 1}"
        )

    pyproject_config["tool"]["poetry"]["version"] = version
    set_pyproject_config(pyproject_config)


def commit_and_tag():
    cmd_commit = ["git", "commit"]
    subprocess.run(cmd_commit, check=True)  # noqa: S603
    cmd_tag = ["git", "tag"]
    subprocess.run(cmd_tag, check=True)  # noqa: S603


if __name__ == "__main__":
    update_changelog("1.0.0", get_current_version(), get_repo_url())
