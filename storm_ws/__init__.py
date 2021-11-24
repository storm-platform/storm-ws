# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-ws is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SpatioTemporal Open Research Manager Web Service."""

from .ext import StormWS
from .version import __version__

__all__ = (
    # Extension initializer
    "StormWS",
    # Package metadata
    "__version__",
)
