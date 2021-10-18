#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Records services`."""

from invenio_drafts_resources.services import RecordService


class NodeService(RecordService):

    def __init__(self, config, files_service=None, draft_files_service=None, project_service=None):
        """Initializer for NodeDraftRecordService."""
        super().__init__(config, files_service, draft_files_service)
        self._project_service = project_service


__all__ = (
    "NodeService"
)
