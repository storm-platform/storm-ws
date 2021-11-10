#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Services components`."""

from flask import g

import werkzeug.exceptions as werkzeug_exceptions

from invenio_records_resources.services.files import FileServiceComponent
from invenio_drafts_resources.services.records.components import ServiceComponent as DraftServiceComponent


class BaseNodeComponent:
    def _populate_node_record(self, data=None, record=None):
        """Populate a node record object based on another record (Draft or Publised)."""
        # Data files
        datafiles = data.get("data", {})
        record.inputs = datafiles.get("inputs", [])
        record.outputs = datafiles.get("outputs", [])

        # Environment
        record.environment = data.get("environment", {})

        # Commands
        record.command = data.get("command")
        record.command_checksum = data.get("command_checksum")


class CompendiumRecordParentServiceComponent(DraftServiceComponent):
    """Component for CompendiumParent project control."""

    def create(self, identity, data=None, record=None, errors=None):
        super().create(identity, data=None, record=None, errors=None)

        # add project on parent object
        record.parent.project_id = g.project_id


class CompendiumRecordDefinitionServiceComponent(BaseNodeComponent, DraftServiceComponent):
    """Component for Compendium Record attributes definitions control."""

    def create(self, identity, data=None, record=None, errors=None):
        self._populate_node_record(data, record)

    def publish(self, identity, draft=None, record=None):
        """Publish handler."""
        self._populate_node_record(draft, record)

    def edit(self, identity, draft=None, record=None):
        """Edit a record handler."""
        self._populate_node_record(record, draft)

    def new_version(self, identity, draft=None, record=None):
        """New version handler."""
        self._populate_node_record(record, draft)


class CompendiumDraftFileDefinitionValidatorComponent(FileServiceComponent):
    """Component to control the Compendium Record attributes definitions."""

    def init_files(self, id_, identity, record, data):
        """Init files handler."""
        self.service.check_draft_files(id_, identity, data)


class BaseProjectValidatorComponent:
    """Base Component for User-Project relation validations."""

    def __init__(self, service, *args, **kwargs):
        """Constructor."""
        self.service = service

    def _check_recordproject(self, record):
        """Check if the record is associated to the requested Project."""
        if record:
            if not (record.parent.project_id == g.project_id):
                raise werkzeug_exceptions.NotFound(
                    description="The requested resource does not exist in the current project.")


class ProjectValidatorRecordServiceComponent(BaseNodeComponent, BaseProjectValidatorComponent):
    """Component to validate User-Project relation."""

    def read(self, identity, **kwargs):
        """Read handler."""
        self._check_recordproject(kwargs.get("record"))

    def update(self, identity, **kwargs):
        """Update handler."""
        self._check_recordproject(kwargs.get("record"))

    def delete(self, identity, **kwargs):
        """Delete handler."""
        self._check_recordproject(kwargs.get("record"))

    def read_draft(self, identity, draft=None):
        """Update draft handler."""
        self._check_recordproject(draft)

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Update draft handler."""
        self._check_recordproject(record)

        self._populate_node_record(record=record, data=data)

    def delete_draft(self, identity, draft=None, record=None, force=False):
        """Delete draft handler."""
        self._check_recordproject(record)

    def edit(self, identity, draft=None, record=None):
        """Edit a record handler."""
        self._check_recordproject(record)

    def new_version(self, identity, draft=None, record=None):
        """New version handler."""
        self._check_recordproject(record)

    def publish(self, identity, draft=None, record=None):
        """Publish handler."""
        self._check_recordproject(record)

    def import_files(self, identity, draft=None, record=None):
        """Import files handler."""
        self._check_recordproject(record)


class ProjectValidatorFileServiceComponent(BaseProjectValidatorComponent, FileServiceComponent):

    def list_files(self, id_, identity, record):
        """List files handler."""
        self._check_recordproject(record)

    def init_files(self, id_, identity, record, data):
        """Init files handler."""
        self._check_recordproject(record)

    def update_file_metadata(self, id_, file_key, identity, record, data):
        """Update file metadata handler."""
        self._check_recordproject(record)

    def read_file_metadata(self, id_, file_key, identity, record):
        """Read file metadata."""
        self._check_recordproject(record)

    def extract_file_metadata(
        self, id_, file_key, identity, record, file_record):
        """Extract file metadata handler."""
        self._check_recordproject(record)

    def commit_file(self, id_, file_key, identity, record):
        """Commit file handler."""
        self._check_recordproject(record)

    def delete_file(self, id_, file_key, identity, record, deleted_file):
        """Delete file handler."""
        self._check_recordproject(record)

    def delete_all_file(self, id_, file_key, identity, record, results):
        """Delete all files handler."""
        self._check_recordproject(record)

    def set_file_content(
        self, id_, file_key, identity, stream, content_length, record):
        """Set file content handler."""
        self._check_recordproject(record)

    def get_file_content(self, id_, file_key, identity, record):
        """Get file content handler."""
        self._check_recordproject(record)


__all__ = (
    "CompendiumRecordParentServiceComponent",
    "CompendiumRecordDefinitionServiceComponent",
    "CompendiumDraftFileDefinitionValidatorComponent",
    "ProjectValidatorRecordServiceComponent",
    "ProjectValidatorFileServiceComponent"
)
