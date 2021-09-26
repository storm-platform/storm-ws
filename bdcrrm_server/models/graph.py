#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `ProjectGraph Models`."""

from invenio_drafts_resources.records import (
    DraftMetadataBase, ParentRecordMixin, ParentRecordStateMixin, Draft, Record
)
from invenio_drafts_resources.records.api import ParentRecord as ParentRecordBase
from invenio_files_rest.models import Bucket
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.records.systemfields import HasDraftCheckField
from invenio_records.dumpers import ElasticsearchDumper
from invenio_records.models import RecordMetadataBase
from invenio_records.systemfields import ModelField, DictField, ConstantField
from invenio_records_resources.records import FileRecordModelMixin
from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields import PIDStatusCheckField, FilesField, IndexField
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils.types import UUIDType
from werkzeug.local import LocalProxy

from . import db
from .base import BaseModel
from ..config import BaseConfiguration


class ProjectGraph(BaseModel, db.Model):
    """SQLAlchemy ProjectGraph model."""

    __tablename__ = "project_graph"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    graph = db.Column(JSONB, nullable=False)


#
# Invenio Records Base models
#
class NodeParentMetadata(BaseModel, db.Model, RecordMetadataBase):
    """Metadata store for the parent record."""

    __tablename__ = 'node_parents_metadata'

    project_id = db.Column(
        db.ForeignKey(f"{BaseConfiguration.BDCRRM_DB_SCHEMA}.project.id", onupdate="CASCADE", ondelete="CASCADE"))

    project = db.relationship("Project", lazy="joined")


class NodeRecordMetadata(BaseModel, db.Model, RecordMetadataBase, ParentRecordMixin):
    """Represent a bibliographic record metadata."""

    __tablename__ = 'node_records_metadata'
    __parent_record_model__ = NodeParentMetadata

    # Enable versioning
    __versioned__ = {}

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class NodeFileRecordMetadata(BaseModel, db.Model, RecordMetadataBase, FileRecordModelMixin):
    """File associated with a record."""

    __tablename__ = 'node_records_files'
    __record_model_cls__ = NodeRecordMetadata


class NodeDraftMetadata(BaseModel, db.Model, DraftMetadataBase, ParentRecordMixin):
    """Draft metadata for a record."""

    __tablename__ = 'node_drafts_metadata'
    __parent_record_model__ = NodeParentMetadata

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class NodeFileDraftMetadata(BaseModel, db.Model, RecordMetadataBase, FileRecordModelMixin):
    """File associated with a draft."""

    __tablename__ = 'node_drafts_files'
    __record_model_cls__ = NodeDraftMetadata


class NodeVersionsState(BaseModel, db.Model, ParentRecordStateMixin):
    """Store for the version state of the parent record."""

    __tablename__ = 'node_versions_state'

    __parent_record_model__ = NodeParentMetadata
    __record_model__ = NodeRecordMetadata
    __draft_model__ = NodeDraftMetadata


#
# Invenio Records API Models (Models with High level operations)
#
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
