"""
    tests.test_python_test
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for module: python_test

    :copyright: (c) 2019-2020, Christian Riedel and AUTHORS
    :license: GPL-3.0, see LICENSE for details
"""  # noqa: D205,D208,D400
import python_test_cielquan

from python_test_cielquan.python_tester import some_func


def test_dummy() -> None:
    """Test a dummy to silence pytest exit code 5."""
    print(python_test_cielquan)

    result = 1 + 1

    assert result == 2


def test_something() -> None:
    """docstring."""
    test_val = 1

    result = some_func(test_val)

    assert result == 2


def test_init() -> None:
    """docstring."""
    result = python_test_cielquan.__version__

    assert result
