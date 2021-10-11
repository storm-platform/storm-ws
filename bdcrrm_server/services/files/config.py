#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Files services config`."""
from invenio_drafts_resources.services.records.config import is_record
from invenio_records_resources.services import FileServiceConfig as BaseFileServiceConfig, RecordLink, FileLink, \
    ConditionalLink

from ..components import (
    ProjectValidatorFileServiceComponent,
    NodeDraftFileDefinitionValidatorComponent
)
from ..links import NodeRecordLink, NodeFileLink
from ...models import NodeDraft, NodeRecord
from ...security import AuthenticatedUserPermissionPolicy


def file_record_is_draft(file, ctx):
    """Shortcut for links to determine if record is a record."""
    return file.record.is_draft


class FileCommonServiceConfig(BaseFileServiceConfig):
    permission_policy_cls = AuthenticatedUserPermissionPolicy

    components = BaseFileServiceConfig.components + [
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
