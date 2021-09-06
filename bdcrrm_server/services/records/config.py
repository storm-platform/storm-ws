#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records Services config`."""

from invenio_drafts_resources.services import RecordServiceConfig as DraftServiceConfigBase
from invenio_drafts_resources.services.records.components import \
    DraftFilesComponent
from invenio_records_resources.services import RecordServiceConfig as RecordServiceConfigBase

from ..components import NodeRecordDefinitionServiceComponent, NodeRecordParentServiceComponent, \
    ProjectValidatorRecordServiceComponent
from ...forms import NodeRecordSchema
from ...indexer import DraftDummyIndexer, RecordDummyIndexer
from ...models import NodeRecord, NodeDraft
from ...security import AuthenticatedUserPermissionPolicy


class NodeCommonServiceConfig(DraftServiceConfigBase):
    record_cls = NodeRecord

    schema = NodeRecordSchema
    permission_policy_cls = AuthenticatedUserPermissionPolicy


class NodeDraftServiceConfig(NodeCommonServiceConfig):
    draft_cls = NodeDraft

    indexer_cls = DraftDummyIndexer

    components = DraftServiceConfigBase.components + [
        DraftFilesComponent,
        NodeRecordParentServiceComponent,
        NodeRecordDefinitionServiceComponent,
        ProjectValidatorRecordServiceComponent
    ]


class NodeRecordServiceConfig(RecordServiceConfigBase):
    indexer_cls = RecordDummyIndexer

    components = RecordServiceConfigBase.components + [
        NodeRecordParentServiceComponent,
        NodeRecordDefinitionServiceComponent,
        ProjectValidatorRecordServiceComponent
    ]


__all__ = (
    "NodeDraftServiceConfig",
    "NodeRecordServiceConfig"
)
