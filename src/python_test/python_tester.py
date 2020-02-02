#!/usr/bin/env python3

# ==============================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'python_tester.py' created 2020-01-19
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
"""docstring"""
import sys


def testus(zahl=2):
    """
    func
    :param zahl: default: 2
    :return: 2 * zahl
    """
    __py_min_ver__ = (3, 7)

    if sys.version_info < __py_min_ver__:
        return 2 * zahl
    return 2 * zahl
