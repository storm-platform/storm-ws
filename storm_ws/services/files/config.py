#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Files services config`."""

from invenio_drafts_resources.services.records.config import is_record
from invenio_records_resources.services import FileServiceConfig, ConditionalLink

from ..components import (
    ProjectValidatorFileServiceComponent,
    NodeDraftFileDefinitionValidatorComponent
)

from ...models import NodeDraft, NodeRecord
from ..links import NodeRecordLink, NodeFileLink
from ..permission import NodeRecordPermissionPolicy


def file_record_is_draft(file, ctx):
    """Shortcut for links to determine if record is a record."""
    return file.record.is_draft


class FileCommonServiceConfig(FileServiceConfig):
    permission_policy_cls = NodeRecordPermissionPolicy

    components = FileServiceConfig.components + [
        ProjectValidatorFileServiceComponent
    ]

    file_links_list = {
        "self": ConditionalLink(
            cond=is_record,
            if_=NodeRecordLink("{+api}graph/{project_id}/node/{id}/files{?args*}"),
            else_=NodeRecordLink("{+api}graph/{project_id}/node/{id}/draft/files{?args*}"),
        ),
    }

    file_links_item = {
        "self": ConditionalLink(
            cond=file_record_is_draft,
            if_=NodeFileLink("{+api}graph/{project_id}/node/{id}/draft/files{?args*}"),
            else_=NodeFileLink("{+api}graph/{project_id}/node/{id}/files{?args*}"),
        ),
        "content": ConditionalLink(
            cond=file_record_is_draft,
            if_=NodeFileLink("{+api}graph/{project_id}/node/{id}/draft/files/{key}/content{?args*}"),
            else_=NodeFileLink("{+api}graph/{project_id}/node/{id}/files/{key}/content{?args*}"),
        ),
        "commit": NodeFileLink("{+api}graph/{project_id}/node/{id}/draft/files/{key}/commit{?args*}",
                               when=file_record_is_draft)
    }


class FileNodeDraftServiceConfig(FileCommonServiceConfig):
    record_cls = NodeDraft
    permission_action_prefix = "draft_"

    components = FileCommonServiceConfig.components + [
        NodeDraftFileDefinitionValidatorComponent,
    ]


class FileNodeRecordServiceConfig(FileCommonServiceConfig):
    record_cls = NodeRecord


__all__ = (
    "FileCommonServiceConfig",
    "FileNodeDraftServiceConfig",
    "FileNodeRecordServiceConfig"
)
