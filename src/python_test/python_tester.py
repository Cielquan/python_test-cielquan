# noqa: D205,D208,D400
"""docstring."""
import sys


def testus(zahl: int = 2) -> int:
    """Line.

    func
    :param zahl: default: 2
    :return: 2 * zahl
    """
    __py_min_ver__ = (3, 7)

    if sys.version_info < __py_min_ver__:
        return 2 * zahl
    return 2 * zahl
