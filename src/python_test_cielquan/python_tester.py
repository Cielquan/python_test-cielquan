"""docstring."""
import sys


def test_us(number: int = 2) -> int:
    """Line.

    func
    :param number: default: 2
    :return: 2 * number
    """
    __py36__ = (3, 6)
    __py37__ = (3, 7)

    if sys.version_info[0:2] == __py36__:  # cover: py36
        return 2 * number
    if sys.version_info[0:2] == __py37__:  # cover: py37
        return 2 * number
    return 2 * number  # cover: py-gte-38


if __name__ == "__main__":
    test_us(1)
