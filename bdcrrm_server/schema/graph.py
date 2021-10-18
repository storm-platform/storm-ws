#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Graph Marshmallow`."""

from marshmallow import Schema, fields
from invenio_drafts_resources.services.records.schema import RecordSchema, ParentSchema


class InvenioFileSchema(Schema):
    """Marshmallow Invenio File definition schema."""
    key = fields.String(required=True)


class NodeRecordMetadata(Schema):
    """Marshmallow Invenio File definition schema."""
    author = fields.String(required=True)
    description = fields.String(required=False)


class NodeRecordFiles(Schema):
    """Marshmallow metadata for Node Record on invenio-records."""
    inputs = fields.List(cls_or_instance=fields.Nested(InvenioFileSchema()), required=True)
    outputs = fields.List(cls_or_instance=fields.Nested(InvenioFileSchema()), required=True)


class NodeParentSchema(ParentSchema):
    """Marshmallow metadata for Node Parent on invenio-records."""


class NodeRecordSchema(RecordSchema):
    """Marshmallow schema for Node Record on invenio-records."""
    data = fields.Nested(NodeRecordFiles(), required=True)

    environment = fields.Nested(InvenioFileSchema(), required=True)

    command = fields.String(required=True)
    command_checksum = fields.String(required=True)

    metadata = fields.Nested(NodeRecordMetadata(), required=True)


__all__ = (
    "InvenioFileSchema",
    "NodeRecordMetadata",
    "NodeRecordFiles",
    "NodeRecordSchema",
    "NodeParentSchema"
)
