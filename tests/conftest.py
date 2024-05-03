"""
    tests.conftest
    ~~~~~~~~~~~~~~

    Init file for test suit.

    :copyright: (c) 2019-2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400

from __future__ import annotations

import pytest


@pytest.fixture
def test_fixture() -> str:
    """Test fixture."""
    return "test"
