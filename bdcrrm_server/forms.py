#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Marshmallow schemas."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields, validate


class ProjectMetadataLicensesForm(Schema):
    """Marshmallow project licenses structure."""
    code = fields.String(required=True)
    data = fields.String(required=True)
    text = fields.String(required=True)


class ProjectMetadataForm(Schema):
    """Marshmallow project metadata structure."""
    licenses = fields.Nested(ProjectMetadataLicensesForm(), required=True)

    author_or_org = fields.String(required=True)
    author_or_org_email = fields.String(required=True)


class ProjectForm(Schema):
    """Marshmallow project structure."""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=False)

    is_public = fields.Boolean(required=True)
    is_finished = fields.Boolean(required=False)

    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)

    graph_id = fields.Integer(required=False)
    metadata = fields.Nested(ProjectMetadataForm(), required=True)


class GraphNodeMetadata(Schema):
    """Marshamllow Node Metadata structure."""
    inputs = fields.List(cls_or_instance=fields.String(), required=True)
    outputs = fields.List(cls_or_instance=fields.String(), required=True)

    repropack = fields.String(required=True)
    updated_in = fields.DateTime(required=False)

    status = fields.String(validate=validate.OneOf(["updated", "outdated"]), required=True)

    command = fields.String(required=True)
    command_checksum = fields.String(required=True)

    inputs_to_define = fields.List(cls_or_instance=fields.String(), required=True)


class GraphNodeForm(Schema):
    """Marshamllow Graph node structure."""
    label = fields.String(required=False)
    metadata = fields.Nested(GraphNodeMetadata(), required=False)


class GraphEdgeForm(fields.Field):
    """Marshamllow Graph Edge structure."""
    source = fields.String(required=True)
    target = fields.String(required=True)


class GraphForm(Schema):
    """Marshmallow Project Graph structure."""
    type = fields.String(required=True)
    directed = fields.Boolean(required=True, validate=validate.Equal(True))

    edges = fields.List(cls_or_instance=GraphEdgeForm(), required=True)
    nodes = fields.Dict(keys=fields.String(), values=fields.Nested(GraphNodeForm()), required=True)


class GraphDocumentForm(Schema):
    """Marshmallow Project Graph structure."""
    graph = fields.Nested(GraphForm(), required=True)


#
# Invenio Framework schemas
#

class InvenioFileSchema(Schema):
    key = fields.String(required=True)


class Metadata(Schema):
    author = fields.String(required=True)
    description = fields.String(required=False)


class NodeRecordFiles(Schema):
    inputs = fields.List(cls_or_instance=fields.Nested(InvenioFileSchema()), required=True)
    outputs = fields.List(cls_or_instance=fields.Nested(InvenioFileSchema()), required=True)


class NodeRecordSchema(BaseRecordSchema):
    data = fields.Nested(NodeRecordFiles(), required=True)

    environment = fields.Nested(InvenioFileSchema(), required=True)

    command = fields.String(required=True)
    command_checksum = fields.String(required=True)

    metadata = fields.Nested(Metadata(), required=True)
