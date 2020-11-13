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

    if sys.version_info[0:2] == __py36__:
        return 2 * zahl
    if sys.version_info[0:2] == __py37__:
        return 2 * zahl
    return 2 * zahl


if __name__ == "__main__":
    testus(1)
