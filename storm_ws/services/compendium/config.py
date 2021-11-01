#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Records services config`."""

from invenio_records_resources.services import ConditionalLink
from invenio_rdm_records.services.components import MetadataComponent
from invenio_drafts_resources.services.records.config import is_draft, is_record

from invenio_drafts_resources.services.records.components import DraftFilesComponent, PIDComponent

from invenio_drafts_resources.services.records.config import RecordServiceConfig, SearchDraftsOptions, SearchOptions

from ..components import (
    CompendiumRecordDefinitionServiceComponent,
    CompendiumRecordParentServiceComponent,
    ProjectValidatorRecordServiceComponent
)

from ..links import CompendiumRecordLink, compendium_pagination_links
from ..permission import CompendiumRecordPermissionPolicy
from ...schema import CompendiumRecordSchema
from ...models import CompendiumRecord, CompendiumDraft
from ...schema.compendium import CompendiumParentSchema


class CompendiumServiceConfig(RecordServiceConfig):
    record_cls = CompendiumRecord
    draft_cls = CompendiumDraft

    # API Response schemas
    schema = CompendiumRecordSchema
    schema_parent = CompendiumParentSchema

    # Security policy
    permission_policy_cls = CompendiumRecordPermissionPolicy

    # Search options
    search = SearchOptions
    search_versions = SearchDraftsOptions

    # Components
    components = [
        MetadataComponent,
        DraftFilesComponent,
        PIDComponent,
        CompendiumRecordParentServiceComponent,
        CompendiumRecordDefinitionServiceComponent,
        ProjectValidatorRecordServiceComponent
    ]

    links_item = {
        "self": ConditionalLink(
            cond=is_record,
            if_=CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}{?args*}"),
            else_=CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/draft{?args*}"),
        ),
        "latest": CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/versions/latest{?args*}"),
        "draft": CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/draft{?args*}", when=is_record),
        "compendium": CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}{?args*}", when=is_draft),
        "publish": CompendiumRecordLink(
            "{+api}pipeline/{project_id}/compendium/{id}/draft/actions/publish{?args*}",
            when=is_draft
        ),
        "files": ConditionalLink(
            cond=is_record,
            if_=CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/files{?args*}"),
            else_=CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/draft/files{?args*}"),
        ),
        "versions": CompendiumRecordLink("{+api}pipeline/{project_id}/compendium/{id}/versions{?args*}"),
    }

    links_search = compendium_pagination_links("{+api}/pipeline/{id}/compendium{?args*}")

    links_search_drafts = compendium_pagination_links("{+api}/user/pipeline/{project_id}/compendium{?args*}")

    links_search_versions = compendium_pagination_links(
        "{+api}/pipeline/{project_id}/compendium/{id}/versions{?args*}")


__all__ = (
    "CompendiumServiceConfig"
)
