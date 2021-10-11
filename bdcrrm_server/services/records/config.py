#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records services config`."""

from invenio_records_resources.services import ConditionalLink
from invenio_drafts_resources.services.records.config import is_draft, is_record

from invenio_drafts_resources.services.records.components import DraftFilesComponent

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
from ...security import AuthenticatedUserPermissionPolicy


class NodeCommonServiceConfig(DraftServiceConfigBase):
    record_cls = NodeRecord

    schema = NodeRecordSchema
    permission_policy_cls = AuthenticatedUserPermissionPolicy

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


class NodeDraftServiceConfig(NodeCommonServiceConfig):
    draft_cls = NodeDraft

    components = DraftServiceConfigBase.components + [
        DraftFilesComponent,
        NodeRecordParentServiceComponent,
        NodeRecordDefinitionServiceComponent,
        ProjectValidatorRecordServiceComponent
    ]


class NodeRecordServiceConfig(RecordServiceConfigBase):
    components = RecordServiceConfigBase.components + [
        NodeRecordParentServiceComponent,
        NodeRecordDefinitionServiceComponent,
        ProjectValidatorRecordServiceComponent
    ]


__all__ = (
    "NodeDraftServiceConfig",
    "NodeRecordServiceConfig"
)
