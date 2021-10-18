#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Graph Models`."""

from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin
)

from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records import FileRecordModelMixin

from sqlalchemy_utils.types import UUIDType

from .. import db
from ..base import BaseModel
from ...config import BaseConfiguration


class NodeParentMetadata(BaseModel, db.Model, RecordMetadataBase):
    """Metadata store for the parent record."""

    __tablename__ = 'node_parents_metadata'

    project_id = db.Column(
        db.ForeignKey(f"{BaseConfiguration.STORM_DB_SCHEMA}.project.id", onupdate="CASCADE", ondelete="CASCADE"))

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


__all__ = (
    "NodeParentMetadata",
    "NodeRecordMetadata",
    "NodeFileRecordMetadata",
    "NodeDraftMetadata",
    "NodeFileDraftMetadata",
    "NodeVersionsState"
)
