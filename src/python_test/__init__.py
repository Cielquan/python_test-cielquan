#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file '__init__.py' created 2020-01-19 is part of the project/program 'python_test'.
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
"""
    matnum
    ~~~~~~

    Handler for siegwerk material numbers.

    ::copyright: (c) Christian Riedel
    :license: MIT, see LICENSE for more details
"""
try:
    from .version import __version__
except ModuleNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"


from .matnum import MatNumHandler


__all__ = (
    "__version__",
    "MatNumHandler",
)
