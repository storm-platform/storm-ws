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
from ..services.files.config import FileNodeDraftServiceConfig, FileNodeRecordServiceConfig
from ..services.files.service import NodeFileService
from ..services.records.config import NodeDraftServiceConfig, NodeRecordServiceConfig
from ..services.records.service import NodeDraftService, NodeRecordService

#
# Files (Draft)
#
file_draft_service = NodeFileService(FileNodeDraftServiceConfig)
file_draft_resource = NodeFileResource(FileNodeDraftResourceConfig, file_draft_service)

#
# Files (Records)
#
file_record_service = NodeFileService(FileNodeRecordServiceConfig)
file_record_resource = NodeFileResource(FileNodeRecordResourceConfig, file_record_service)

#
# Nodes (Draft)
#
node_draft_service = NodeDraftService(NodeDraftServiceConfig, files_service=file_record_service,
                                      draft_files_service=file_draft_service)
node_draft_resource = NodeDraftResource(NodeDraftResourceConfig, node_draft_service)

#
# Nodes (Records)
#
node_record_service = NodeRecordService(NodeRecordServiceConfig)
node_record_resource = NodeRecordResource(NodeRecordResourceConfig, node_record_service)

__all__ = (
    "node_draft_resource",
    "node_record_resource"
)
