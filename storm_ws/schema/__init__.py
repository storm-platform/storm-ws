#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Marshmallow schemas`."""

from .compendium import (
    InvenioFileSchema,
    CompendiumRecordMetadata,
    CompendiumRecordFiles,
    CompendiumRecordSchema
)

from .project import (
    ProjectMetadataLicensesSchema,
    ProjectMetadataSchema,
    ProjectSchema,
    ProjectPipelineCompendiumSchema,
    ProjectPipelineConnectionField,
    ProjectPipelineField,
    ProjectPipelineSchema,
    ProjectPipelineDefinitionMetadata,
    ProjectPipelineDefinitionSchema,
    ProjectMultiPipelineSchema
)

__all__ = (
    "InvenioFileSchema",
    "CompendiumRecordMetadata",
    "CompendiumRecordFiles",
    "CompendiumRecordSchema",

    "ProjectMetadataLicensesSchema",
    "ProjectMetadataSchema",
    "ProjectSchema",
    "ProjectPipelineCompendiumSchema",
    "ProjectPipelineConnectionField",
    "ProjectPipelineField",
    "ProjectPipelineSchema",
    "ProjectPipelineDefinitionMetadata",
    "ProjectPipelineDefinitionSchema",
    "ProjectMultiPipelineSchema"
)
