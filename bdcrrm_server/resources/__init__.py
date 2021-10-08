#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Resources`."""

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
    NodeDraftResourceConfig,
    NodeRecordResourceConfig,
    NodeRecordResource,
    NodeDraftResource
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
    "NodeDraftResourceConfig",
    "NodeRecordResourceConfig",

    "FileNodeDraftResourceConfig",
    "FileNodeRecordResourceConfig",

    "NodeFileResource",
    "NodeDraftResource",
    "NodeRecordResource",

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