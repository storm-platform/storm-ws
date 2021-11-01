#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Execution Compendium Marshmallow`."""

from marshmallow import Schema, fields
from invenio_drafts_resources.services.records.schema import RecordSchema, ParentSchema


class InvenioFileSchema(Schema):
    """Marshmallow Invenio File definition schema."""
    key = fields.String(required=True)


class CompendiumRecordMetadata(Schema):
    """Marshmallow Invenio File definition schema."""
    author = fields.String(required=True)
    description = fields.String(required=False)


class CompendiumRecordFiles(Schema):
    """Marshmallow metadata for Node Record on invenio-compendium."""
    inputs = fields.List(cls_or_instance=fields.Nested(InvenioFileSchema()), required=True)
    outputs = fields.List(cls_or_instance=fields.Nested(InvenioFileSchema()), required=True)


class CompendiumParentSchema(ParentSchema):
    """Marshmallow metadata for Node Parent on invenio-compendium."""


class CompendiumRecordSchema(RecordSchema):
    """Marshmallow schema for Node Record on invenio-compendium."""
    data = fields.Nested(CompendiumRecordFiles(), required=True)

    environment = fields.Nested(InvenioFileSchema(), required=True)

    command = fields.String(required=True)
    command_checksum = fields.String(required=True)

    metadata = fields.Nested(CompendiumRecordMetadata(), required=True)


__all__ = (
    "InvenioFileSchema",
    "CompendiumRecordMetadata",
    "CompendiumRecordFiles",
    "CompendiumRecordSchema",
    "CompendiumParentSchema"
)
