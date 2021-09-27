#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records services`."""

from invenio_records_resources.services import RecordService as RecordServiceBase
from invenio_drafts_resources.services import RecordService as RecordDraftServiceBase


class NodeRecordService(RecordServiceBase):

    def __init__(self, config, project_service=None):
        """Constructor for RecordService."""
        super().__init__(config)
        self._project_service = project_service


class NodeDraftService(RecordDraftServiceBase):

    def __init__(self, config, files_service=None, draft_files_service=None, project_service=None):
        """Initializer for NodeDraftRecordService."""
        super().__init__(config, files_service, draft_files_service)
        self._project_service = project_service


__all__ = (
    "NodeRecordService",
    "NodeDraftService"
)
