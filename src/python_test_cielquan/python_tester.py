"""docstring."""
import sys


def some_func(number: int = 2) -> int:
    """Line.

    func
    :param number: default: 2
    :return: 2 * number
    """
    __py36__ = (3, 6)
    __py37__ = (3, 7)

    if sys.version_info[0:2] == __py36__:  # pragma: py36
        return 2 * number
    if sys.version_info[0:2] == __py37__:  # pragma: py37
        return 2 * number
    return 2 * number  # pragma: py-gte-38


if __name__ == "__main__":
    some_func(1)
