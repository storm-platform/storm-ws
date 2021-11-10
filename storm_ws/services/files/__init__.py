#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Files services module`."""

from .config import (
    FileNodeDraftServiceConfig,
    FileNodeRecordServiceConfig
)

from .service import (
    CompendiumFileService,
    CompendiumFileDraftService
)

__all__ = (
    "FileNodeDraftServiceConfig",
    "FileNodeRecordServiceConfig",

    "CompendiumFileService",
    "CompendiumFileDraftService"
)
