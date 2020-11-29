"""
    python_test-cielquan
    ~~~~~~~~~~~~~~~~~~~~

    Test repo for python stuff

    :copyright: (c) Christian Riedel
    :license: MIT, see LICENSE for more details
"""  # noqa: D205,D208,D400
try:
    from importlib.metadata import metadata
except ModuleNotFoundError:
    from importlib_metadata import metadata  # type: ignore[import,no-redef]


md = dict(metadata(__name__))


__author__ = md["Author"]
__license__ = md["License"]
__project__ = md["Name"]
__version__ = md["Version"]
version_info = tuple(__version__.split("."))

__gh_repository_link__ = md["Project-URL"].replace("Repository, ", "")
__gh_repository__ = __gh_repository_link__.replace("https://github.com/", "")
