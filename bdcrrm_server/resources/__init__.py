#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Resources`."""

from .files.config import FileNodeDraftResourceConfig, FileNodeRecordResourceConfig
from .files.resource import NodeFileResource
from .records.config import NodeDraftResourceConfig, NodeRecordResourceConfig
from .records.resource import NodeRecordResource, NodeDraftResource

from .server import ServerResource, ServerResourceConfig

__all__ = (
    "NodeDraftResourceConfig",
    "NodeRecordResourceConfig",

    "FileNodeDraftResourceConfig",
    "FileNodeRecordResourceConfig",

    "NodeFileResource",
    "NodeDraftResource",
    "NodeRecordResource",

    "ServerResource",
    "ServerResourceConfig"
)
