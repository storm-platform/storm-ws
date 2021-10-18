#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project services`."""

from invenio_records_resources.services import FileService


class NodeFileService(FileService):
    def __init__(self, config, project_service=None):
        """Constructor for NodeFileService."""
        super().__init__(config)
        self._project_service = project_service


class NodeFileDraftService(NodeFileService):
    def check_draft_files(self, id_, identity, file_keys):
        """Check draft files that will be defined.

        In this method, the input file keys are validated with the record files. If the file key
        is not defined on record, the method will be raise a exception.
        """
        # Resolve and require permission
        draft = self.record_cls.pid.resolve(id_, registered_only=False)

        # Run components
        for component in self.components:
            if hasattr(component, 'read_draft'):
                component.read_draft(identity, draft=draft)

        files = [f['key'] for f in [*draft.inputs, *draft.outputs, *[draft.environment]]]

        for file_key in file_keys:
            if file_key["key"] not in files:
                raise RuntimeError("File is not defined for this Node.")


__all__ = (
    "NodeFileService",
    "NodeFileDraftService"
)
