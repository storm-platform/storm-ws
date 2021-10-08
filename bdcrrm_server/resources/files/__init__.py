#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Files resources module`."""

from .resource import NodeFileResource

from .config import (
    FileNodeDraftResourceConfig,
    FileNodeRecordResourceConfig
)

__all__ = (
    "NodeFileResource",
    "FileNodeDraftResourceConfig",
    "FileNodeRecordResourceConfig"
)