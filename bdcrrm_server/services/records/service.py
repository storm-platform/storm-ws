#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_drafts_resources.services import RecordService as RecordDraftServiceBase
from invenio_records_resources.services import RecordService as RecordServiceBase


class NodeRecordService(RecordServiceBase):
    ...


class NodeDraftService(RecordDraftServiceBase):

    def check_draft_files(self, id_, identity, file_key):
        """Retrieve a draft."""
        # Resolve and require permission
        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        self.require_permission(identity, "read_draft", record=draft)

        # Run components
        for component in self.components:
            if hasattr(component, 'read_draft'):
                component.read_draft(identity, draft=draft)

        files = [f['key'] for f in [*draft.inputs, *draft.outputs, *draft.environment]]
        if file_key not in files:
            raise RuntimeError("File is not defined for this Node.")
