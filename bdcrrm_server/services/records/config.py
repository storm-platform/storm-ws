#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records services config`."""

from invenio_records_resources.services import ConditionalLink, pagination_links
from invenio_drafts_resources.services.records.config import (
    SearchOptions, SearchVersionsOptions, is_draft, is_record
)

from invenio_drafts_resources.services.records.components import DraftFilesComponent, DraftMetadataComponent, \
    PIDComponent

from invenio_drafts_resources.services import RecordServiceConfig as DraftServiceConfigBase
from invenio_records_resources.services import RecordServiceConfig as RecordServiceConfigBase

from ..components import (
    NodeRecordDefinitionServiceComponent,
    NodeRecordParentServiceComponent,
    ProjectValidatorRecordServiceComponent
)

from ..links import NodeRecordLink
from ...schema import NodeRecordSchema
from ...models import NodeRecord, NodeDraft
from ...schema.graph import NodeParentSchema
from ...security import AuthenticatedUserPermissionPolicy


class NodeServiceConfig(DraftServiceConfigBase):
    record_cls = NodeRecord
    draft_cls = NodeDraft

    # API Response schemas
    schema = NodeRecordSchema
    schema_parent = NodeParentSchema

    # Security policy
    permission_policy_cls = AuthenticatedUserPermissionPolicy

    # Components
    components = [
        DraftMetadataComponent,
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

    links_search = pagination_links("{+api}/graph/{project_id}/node{?args*}")

    links_search_drafts = pagination_links("{+api}/user/graph/{project_id}/node{?args*}")

    links_search_versions = pagination_links(
        "{+api}/graph/{project_id}/node/{id}/versions{?args*}")


__all__ = (
    "NodeServiceConfig"
)
