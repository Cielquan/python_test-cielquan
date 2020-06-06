# noqa: D205,D208,D400
"""
    matnum
    ~~~~~~

    Handler for siegwerk material numbers.

    ::copyright: (c) Christian Riedel
    :license: MIT, see LICENSE for more details
"""
try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version  # type: ignore

__version__ = version(__name__)
