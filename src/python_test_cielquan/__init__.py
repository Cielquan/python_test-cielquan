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


md = dict(metadata(__name__))


__author__ = md["Author"]
__license__ = md["License"]
__project__ = md["Name"]
__version__ = md["Version"]
version_info = tuple(__version__.split("."))

__gh_repository_link__ = md["Project-URL"].replace("Repository, ", "")
__gh_repository__ = __gh_repository_link__.replace("https://github.com/", "")
