#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Graph Marshmallow.."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields


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


class NodeRecordSchema(BaseRecordSchema):
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
    "NodeRecordSchema"
)
