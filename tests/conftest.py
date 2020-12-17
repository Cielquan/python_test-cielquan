"""
    tests.conftest
    ~~~~~~~~~~~~~~

    Init file for test suit.

    :copyright: (c) Christian Riedel
    :license: MIT, see LICENSE for more details
"""  # noqa: D205,D208,D400
import pytest


@pytest.fixture
def test_fixture() -> str:
    """Test fixture."""
    return "test"
