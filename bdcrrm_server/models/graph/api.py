#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Graph API`."""

from invenio_drafts_resources.records import (
    Draft, Record
)

from werkzeug.local import LocalProxy

from invenio_pidstore.models import PIDStatus
from invenio_records.dumpers import ElasticsearchDumper
from invenio_rdm_records.records.systemfields import HasDraftCheckField

from invenio_records_resources.records.api import FileRecord

from invenio_records.systemfields import (
    ModelField,
    DictField,
    ConstantField
)

from invenio_records_resources.records.systemfields import (
    PIDStatusCheckField,
    FilesField,
    IndexField
)

from bdcrrm_server.models.graph.models import (
    NodeParentMetadata,
    NodeVersionsState,
    NodeFileDraftMetadata,
    NodeDraftMetadata,
    NodeFileRecordMetadata,
    NodeRecordMetadata
)

from invenio_drafts_resources.records.api import ParentRecord as ParentRecordBase


class NodeParent(ParentRecordBase):
    """Node Parent record."""

    model_cls = NodeParentMetadata

    project_id = ModelField(dump=False)
    project = ModelField(dump=False)

    dumper = ElasticsearchDumper()

    schema = ConstantField(
        "$schema", "local://records/nodeparent-v1.0.0.json"
    )


class CommonFieldsMixin:
    """Common system fields between records and drafts."""

    versions_model_cls = NodeVersionsState
    parent_record_cls = NodeParent

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)

    inputs = DictField("data.inputs")
    outputs = DictField("data.outputs")

    environment = DictField("environment")

    command = DictField("command")
    command_checksum = DictField("command_checksum")

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)
    pids = DictField("pids")

    dumper = ElasticsearchDumper()
    schema = ConstantField(
        '$schema', 'local://records/noderecord-v1.0.0.json')


class NodeFileDraft(FileRecord):
    model_cls = NodeFileDraftMetadata
    record_cls = LocalProxy(lambda: NodeDraft)


class NodeDraft(CommonFieldsMixin, Draft):
    model_cls = NodeDraftMetadata

    index = IndexField("node-drafts-draft-v1.0.0")

    files = FilesField(
        store=False,
        file_cls=NodeFileDraft,
        delete=False
    )

    has_draft = HasDraftCheckField()


class NodeFileRecord(FileRecord):
    model_cls = NodeFileRecordMetadata
    record_cls = LocalProxy(lambda: NodeRecord)


class NodeRecord(CommonFieldsMixin, Record):
    model_cls = NodeRecordMetadata

    index = IndexField("node-records-record-v1.0.0")

    files = FilesField(
        store=False,
        file_cls=NodeFileRecord,
        create=False,
        delete=False
    )

    has_draft = HasDraftCheckField(NodeDraft)


__all__ = (
    "NodeParent",
    "NodeDraft",
    "NodeFileDraft",
    "NodeRecord",
    "NodeFileRecord"
)
