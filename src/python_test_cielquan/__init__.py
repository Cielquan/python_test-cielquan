"""
    python_test-cielquan
    ~~~~~~~~~~~~~~~~~~~~

    Test repo for python stuff

    :copyright: (c) 2019-2020, Christian Riedel and AUTHORS
    :license: GPL-3.0, see LICENSE for details
"""  # noqa: D205,D208,D400
try:
    from importlib.metadata import metadata
except ModuleNotFoundError:  # pragma: py-gte-38
    from importlib_metadata import metadata  # type: ignore[import,no-redef]


md = metadata(__name__)


__author__ = md["Author"]
__license__ = md["License"]
__project__ = md["Name"]
__version__ = md["Version"]
version_info = tuple(__version__.split("."))


#: Extract Project-URLs from metadata
urls = (line[13:] for line in str(md).split("\n") if line.startswith("Project-URL"))
url_map = {url[: url.find(",")]: url[url.find("http") :] for url in urls}


#: Search for and set a link to GH repo
__gh_repository_link__ = None
for cat in ("Github", "Repository", "Source", "Code", "Homepage"):
    if cat in url_map:
        __gh_repository_link__ = url_map[cat].rstrip("/")
        __gh_repository__ = __gh_repository_link__.replace("https://github.com/", "")
        break

if __gh_repository_link__ is None:
    raise AttributeError("Metadata do not contain a link to source.")
