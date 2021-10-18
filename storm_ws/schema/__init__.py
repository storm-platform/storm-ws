#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Marshmallow schemas`."""

from .graph import (
    InvenioFileSchema,
    NodeRecordMetadata,
    NodeRecordFiles,
    NodeRecordSchema
)

from .project import (
    ProjectMetadataLicensesSchema,
    ProjectMetadataSchema,
    ProjectSchema,
    ProjectGraphNodeSchema,
    ProjectGraphEdgeField,
    ProjectGraphField,
    ProjectGraphSchema,
    ProjectGraphDefinitionMetadata,
    ProjectGraphDefinitionSchema,
    ProjectMultiGraphSchema
)

__all__ = (
    "InvenioFileSchema",
    "NodeRecordMetadata",
    "NodeRecordFiles",
    "NodeRecordSchema",

    "ProjectMetadataLicensesSchema",
    "ProjectMetadataSchema",
    "ProjectSchema",
    "ProjectGraphNodeSchema",
    "ProjectGraphEdgeField",
    "ProjectGraphField",
    "ProjectGraphSchema",
    "ProjectGraphDefinitionMetadata",
    "ProjectGraphDefinitionSchema",
    "ProjectMultiGraphSchema"
)
