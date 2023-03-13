"""
    python_test-cielquan
    ~~~~~~~~~~~~~~~~~~~~

    Test repo for python stuff

    :copyright: (c) 2019-2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400


try:
    from importlib.metadata import metadata as get_md
except ModuleNotFoundError:  # pragma: py-gte-38
    from importlib_metadata import metadata as get_md  # type: ignore[import,no-redef]


def _get_gh_repo_link(metadata_list: list[str]) -> str:
    #: Extract Project-URLs from metadata
    urls = (line[13:] for line in metadata_list if line.startswith("Project-URL"))
    url_map = {url[: url.find(",")]: url[url.find("http") :] for url in urls}

    #: Search for and set a link to Github repo
    for cat in ("Github", "Repository", "Source", "Code", "Homepage"):
        if cat in url_map:
            return url_map[cat].rstrip("/")

    raise AttributeError(  # pragma: no cover
        "Metadata does not contain a link to source code on github."
    )


metadata = get_md(__name__)


__author__ = metadata["Author"]
__license__ = metadata["License"]
__project__ = metadata["Name"]
__version__ = metadata["Version"]
version_info = tuple(__version__.split("."))

__gh_repository_link__ = _get_gh_repo_link(str(metadata).split("\n"))
__gh_repository__ = __gh_repository_link__.replace("https://github.com/", "")
