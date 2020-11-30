"""docstring."""
import python_test_cielquan

from python_test_cielquan.python_tester import some_func


def test_something() -> None:
    """docstring."""
    test_val = 1

    result = some_func(test_val)

    assert result == 2


def test_init() -> None:
    """docstring."""
    result = python_test_cielquan.__version__

    assert result
