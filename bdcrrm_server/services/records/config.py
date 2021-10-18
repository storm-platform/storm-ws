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
    NodeRecordDefinitionServiceComponent,
    NodeRecordParentServiceComponent,
    ProjectValidatorRecordServiceComponent
)

from ..links import NodeRecordLink, node_pagination_links
from ..permission import NodeRecordPermissionPolicy
from ...schema import NodeRecordSchema
from ...models import NodeRecord, NodeDraft
from ...schema.graph import NodeParentSchema


class NodeServiceConfig(RecordServiceConfig):
    record_cls = NodeRecord
    draft_cls = NodeDraft

    # API Response schemas
    schema = NodeRecordSchema
    schema_parent = NodeParentSchema

    # Security policy
    permission_policy_cls = NodeRecordPermissionPolicy

    # Search options
    search = SearchOptions
    search_versions = SearchDraftsOptions

    # Components
    components = [
        MetadataComponent,
        DraftFilesComponent,
        PIDComponent,
        NodeRecordParentServiceComponent,
        NodeRecordDefinitionServiceComponent,
        ProjectValidatorRecordServiceComponent
    ]

    links_item = {
        "self": ConditionalLink(
            cond=is_record,
            if_=NodeRecordLink("{+api}graph/{project_id}/node/{id}{?args*}"),
            else_=NodeRecordLink("{+api}graph/{project_id}/node/{id}/draft{?args*}"),
        ),
        "latest": NodeRecordLink("{+api}graph/{project_id}/node/{id}/versions/latest{?args*}"),
        "draft": NodeRecordLink("{+api}graph/{project_id}/node/{id}/draft{?args*}", when=is_record),
        "record": NodeRecordLink("{+api}graph/{project_id}/node/{id}{?args*}", when=is_draft),
        "publish": NodeRecordLink(
            "{+api}graph/{project_id}/node/{id}/draft/actions/publish{?args*}",
            when=is_draft
        ),
        "files": ConditionalLink(
            cond=is_record,
            if_=NodeRecordLink("{+api}graph/{project_id}/node/{id}/files{?args*}"),
            else_=NodeRecordLink("{+api}graph/{project_id}/node/{id}/draft/files{?args*}"),
        ),
        "versions": NodeRecordLink("{+api}graph/{project_id}/node/{id}/versions{?args*}"),
    }

    links_search = node_pagination_links("{+api}/graph/{id}/node{?args*}")

    links_search_drafts = node_pagination_links("{+api}/user/graph/{project_id}/node{?args*}")

    links_search_versions = node_pagination_links(
        "{+api}/graph/{project_id}/node/{id}/versions{?args*}")


__all__ = (
    "NodeServiceConfig"
)
