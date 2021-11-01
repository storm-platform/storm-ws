#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Services`."""

from .files import (
    FileNodeDraftServiceConfig,
    FileNodeRecordServiceConfig,
    CompendiumFileService,
    CompendiumFileDraftService
)

from .project import (
    ProjectService,
    ProjectServiceConfig,
    ProjectGraphServiceConfig,
    ProjectPipelineService
)

from .compendium import (
    CompendiumService,
    CompendiumServiceConfig
)

__all__ = (
    "ProjectServiceConfig",
    "FileNodeDraftServiceConfig",
    "FileNodeRecordServiceConfig",

    "CompendiumFileService",
    "CompendiumFileDraftService",

    "ProjectService",

    "CompendiumService",
    "CompendiumServiceConfig",

    "ProjectPipelineService",
    "ProjectGraphServiceConfig"
)
