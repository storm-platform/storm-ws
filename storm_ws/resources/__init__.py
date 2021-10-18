#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Resources`."""

from .files import (
    FileNodeDraftResourceConfig,
    FileNodeRecordResourceConfig,
    NodeFileResource
)

from .project import (
    ProjectResourceConfig,
    ProjectGraphResourceConfig,
    ProjectGraphNodeResourceConfig,

    ProjectResource,
    ProjectGraphResource,
    ProjectGraphNodeResource
)

from .records import (
    NodeResource,
    NodeResourceConfig
)

from .server import (
    ServerResource,
    ServerResourceConfig
)

from .service import (
    ServiceResource,
    ServiceResourceConfig
)

__all__ = (
    "NodeResource",
    "NodeResourceConfig",

    "FileNodeDraftResourceConfig",
    "FileNodeRecordResourceConfig",

    "NodeResource",
    "NodeFileResource",

    "ServerResource",
    "ServerResourceConfig",

    "ServiceResource",
    "ServiceResourceConfig",

    "ProjectResourceConfig",
    "ProjectGraphResourceConfig",
    "ProjectGraphNodeResourceConfig",

    "ProjectResource",
    "ProjectGraphResource",
    "ProjectGraphNodeResource"
)
