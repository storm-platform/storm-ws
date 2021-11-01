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
    CompendiumDraftFileDefinitionValidatorComponent
)

from ...models import CompendiumDraft, CompendiumRecord
from ..links import CompendiumRecordLink, CompendiumFileLink
from ..permission import CompendiumRecordPermissionPolicy


def file_record_is_draft(file, ctx):
    """Shortcut for links to determine if record is a record."""
    return file.record.is_draft


class FileCommonServiceConfig(FileServiceConfig):
    permission_policy_cls = CompendiumRecordPermissionPolicy

    components = FileServiceConfig.components + [
        ProjectValidatorFileServiceComponent
    ]

    file_links_list = {
        "self": ConditionalLink(
            cond=is_record,
            if_=CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/files{?args*}"),
            else_=CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/draft/files{?args*}"),
        ),
    }

    file_links_item = {
        "self": ConditionalLink(
            cond=file_record_is_draft,
            if_=CompendiumFileLink("{+api}pipeline/{project_id}/compendium/{id}/draft/files{?args*}"),
            else_=CompendiumFileLink("{+api}pipeline/{project_id}/compendium/{id}/files{?args*}"),
        ),
        "content": ConditionalLink(
            cond=file_record_is_draft,
            if_=CompendiumFileLink("{+api}pipeline/{project_id}/compendium/{id}/draft/files/{key}/content{?args*}"),
            else_=CompendiumFileLink("{+api}pipeline/{project_id}/compendium/{id}/files/{key}/content{?args*}"),
        ),
        "commit": CompendiumFileLink("{+api}pipeline/{project_id}/compendium/{id}/draft/files/{key}/commit{?args*}",
                                     when=file_record_is_draft)
    }


class FileNodeDraftServiceConfig(FileCommonServiceConfig):
    record_cls = CompendiumDraft
    permission_action_prefix = "draft_"

    components = FileCommonServiceConfig.components + [
        CompendiumDraftFileDefinitionValidatorComponent,
    ]


class FileNodeRecordServiceConfig(FileCommonServiceConfig):
    record_cls = CompendiumRecord


__all__ = (
    "FileCommonServiceConfig",
    "FileNodeDraftServiceConfig",
    "FileNodeRecordServiceConfig"
)
