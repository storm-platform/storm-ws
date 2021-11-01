#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Resources`."""

from .files import (
    FileCompendiumDraftResourceConfig,
    FileCompendiumRecordResourceConfig,
    CompendiumFileResource
)

from .project import (
    ProjectResourceConfig,
    ProjectPipelineResourceConfig,
    ProjectPipelineCompendiumResourceConfig,

    ProjectResource,
    ProjectPipelineResource,
    ProjectPipelineCompendiumResource
)

from .compendium import (
    CompendiumResource,
    CompendiumResourceConfig
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
    "CompendiumResource",
    "CompendiumResourceConfig",

    "FileCompendiumDraftResourceConfig",
    "FileCompendiumRecordResourceConfig",

    "CompendiumResource",
    "CompendiumFileResource",

    "ServerResource",
    "ServerResourceConfig",

    "ServiceResource",
    "ServiceResourceConfig",

    "ProjectResourceConfig",
    "ProjectPipelineResourceConfig",
    "ProjectPipelineCompendiumResourceConfig",

    "ProjectResource",
    "ProjectPipelineResource",
    "ProjectPipelineCompendiumResource"
)
