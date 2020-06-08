# noqa: D205,D208,D400
"""docstring."""
import sys


def testus(zahl: int = 2) -> int:
    """Line.

    func
    :param zahl: default: 2
    :return: 2 * zahl
    """
    __py36__ = (3, 6)
    __py37__ = (3, 7)
    __py38__ = (3, 8)

    if sys.version_info == __py36__:
        return 2 * zahl
    if sys.version_info == __py37__:
        return 2 * zahl
    if sys.version_info == __py38__:
        return 2 * zahl
    return 2 * zahl
