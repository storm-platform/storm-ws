#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Marshmallow schemas."""

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
