#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Services components`."""

from flask import g

from invenio_drafts_resources.services.records.components import ServiceComponent as DraftServiceComponent
from invenio_records_resources.services.files import FileServiceComponent


class NodeRecordParentServiceComponent(DraftServiceComponent):
    """Component for NodeParent project control."""

    def create(self, identity, data=None, record=None, errors=None):
        super().create(identity, data=None, record=None, errors=None)

        # add project on parent object
        record.parent.project_id = g.project_id


class NodeRecordDefinitionServiceComponent(DraftServiceComponent):
    """Component for NodeRecord attributes definitions control."""

    def create(self, identity, data=None, record=None, errors=None):
        super().create(identity, data=None, record=None, errors=None)

        # Data files
        datafiles = data.get("data", {})
        record.inputs = datafiles.get("inputs", [])
        record.outputs = datafiles.get("outputs", [])

        # Environment
        record.environment = data.get("environment", {})

        # Commands
        record.command = data.get("command")
        record.command_checksum = data.get("command_checksum")


class NodeDraftFileDefinitionValidatorComponent(FileServiceComponent):
    """Component to control the NodeRecord attributes definitions."""

    def init_files(self, id_, identity, record, data):
        """Init files handler."""
        self.service.check_draft_files(id_, identity, data)


class BaseProjectValidatorComponent:
    """Base Component for User-Project relation validations."""

    def __init__(self, service, *args, **kwargs):
        """Constructor."""
        self.service = service

    def _check_userproject(self, identity) -> None:
        """Check if the user has permission to access the requested Project.

        Args:
            identity (flask_principal.Identity): User identity

        Raises: When user is not able to access the requested project.
        """
        # FixMe: Remove this dependency relationship between service and component
        # Checking that the project service has been injected as a subservice to avoid errors
        if "_project_service" in dir(self.service):  # avoiding broken errors

            current_project = g.project_id
            user_projects = self.service._project_service.list_project_by_user(identity.id)

            if current_project not in [p.id for p in user_projects]:
                raise RuntimeError("User is not able to access this project.")

    def _check_recordproject(self, record):
        """Check if the record is associated to the requested Project."""
        if record:
            if not (record.parent.project_id == g.project_id):
                raise RuntimeError("The requested resource does not exist in the current project.")


class ProjectValidatorRecordServiceComponent(BaseProjectValidatorComponent):
    """Component to validate User-Project relation."""

    def create(self, identity, **kwargs):
        """Read handler."""
        self._check_userproject(identity)

    def read(self, identity, **kwargs):
        """Read handler."""
        self._check_userproject(identity)
        self._check_recordproject(kwargs.get("record"))

    def update(self, identity, **kwargs):
        """Update handler."""
        self._check_userproject(identity)
        self._check_recordproject(kwargs.get("record"))

    def delete(self, identity, **kwargs):
        """Delete handler."""
        self._check_userproject(identity)
        self._check_recordproject(kwargs.get("record"))

    def read_draft(self, identity, draft=None):
        """Update draft handler."""
        self._check_userproject(identity)
        self._check_recordproject(draft)

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Update draft handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def delete_draft(self, identity, draft=None, record=None, force=False):
        """Delete draft handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def edit(self, identity, draft=None, record=None):
        """Edit a record handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def new_version(self, identity, draft=None, record=None):
        """New version handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def publish(self, identity, draft=None, record=None):
        """Publish handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def import_files(self, identity, draft=None, record=None):
        """Import files handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)


class ProjectValidatorFileServiceComponent(BaseProjectValidatorComponent, FileServiceComponent):

    def list_files(self, id_, identity, record):
        """List files handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def init_files(self, id_, identity, record, data):
        """Init files handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def update_file_metadata(self, id_, file_key, identity, record, data):
        """Update file metadata handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def read_file_metadata(self, id_, file_key, identity, record):
        """Read file metadata."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def extract_file_metadata(
        self, id_, file_key, identity, record, file_record):
        """Extract file metadata handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def commit_file(self, id_, file_key, identity, record):
        """Commit file handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def delete_file(self, id_, file_key, identity, record, deleted_file):
        """Delete file handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def delete_all_file(self, id_, file_key, identity, record, results):
        """Delete all files handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def set_file_content(
        self, id_, file_key, identity, stream, content_length, record):
        """Set file content handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)

    def get_file_content(self, id_, file_key, identity, record):
        """Get file content handler."""
        self._check_userproject(identity)
        self._check_recordproject(record)


__all__ = (
    "NodeRecordParentServiceComponent",
    "NodeRecordDefinitionServiceComponent",
    "NodeDraftFileDefinitionValidatorComponent",
    "ProjectValidatorRecordServiceComponent",
    "ProjectValidatorFileServiceComponent"
)
