"""
    python_test-cielquan.python_tester
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Python source for testing

    :copyright: (c) 2019-2020, Christian Riedel, see AUTHORS
    :license: GPL-3.0, see LICENSE for details
"""  # noqa: D205,D208,D400
import sys


def some_func(number: int = 2) -> int:
    """Line.

    func
    :param number: default: 2
    :return: 2 * number
    """
    __py36__ = (3, 6)
    __py37__ = (3, 7)

    if sys.version_info[0:2] == __py36__:  # pragma: py-ue-36
        return 2 * number
    if sys.version_info[0:2] == __py37__:  # pragma: py-ue-37
        return 2 * number
    return 2 * number  # pragma: py-lt-38


if __name__ == "__main__":
    some_func(1)
