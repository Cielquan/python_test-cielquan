#!/usr/bin/env python3

# ==============================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'test_python_test.py' created 2020-01-19
# is part of the project/program 'python_test'.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published by
# the Massachusetts Institute of Technology.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://opensource.org/licenses/MIT>.
#
# Github: https://github.com/Cielquan/
# ==============================================================================
"""docstring."""
import python_test_cielquan

from python_test_cielquan.python_tester import test_us


def test_something() -> None:
    """docstring."""
    test_val = 1

    result = test_us(test_val)

    assert result == 2


def test_init() -> None:
    """docstring."""
    result = python_test_cielquan.__version__

    assert result
