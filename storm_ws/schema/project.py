#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project Marshmallow`."""

from marshmallow import Schema, fields, validate


class ProjectUserSchema(Schema):
    """Marshmallow project user schema."""
    id = fields.Integer(required=False)
    user_id = fields.Integer(dump_only=True)
    project_id = fields.Integer(dump_only=True)

    active = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)


class ProjectMetadataLicensesSchema(Schema):
    """Marshmallow project licenses schema."""
    code = fields.String(required=True)
    data = fields.String(required=True)
    text = fields.String(required=True)


class ProjectMetadataSchema(Schema):
    """Marshmallow project metadata schema."""
    licenses = fields.Nested(ProjectMetadataLicensesSchema(), required=True)

    author_or_org = fields.String(required=True)
    author_or_org_email = fields.String(required=True)


class ProjectSchema(Schema):
    """Marshmallow Project schema."""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=False)

    is_public = fields.Boolean(required=True)
    is_finished = fields.Boolean(required=False)

    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)

    graph_id = fields.Integer(required=False)
    metadata = fields.Nested(ProjectMetadataSchema(), required=True, load_only=True)
    _metadata = fields.Nested(ProjectMetadataSchema(), required=True, dump_only=True, data_key="metadata")


class ProjectPipelineCompendiumSchema(Schema):
    """Marshamllow ProjectPipelineNodeSchema schema."""
    id = fields.String(required=True)


class ProjectPipelineConnectionField(fields.Field):
    """Marshmallow project pipeline field."""
    source = fields.String(required=True)
    target = fields.String(required=True)


class ProjectPipelineBase:
    """ProjectPipeline base properties."""
    type = fields.String(required=True)
    label = fields.String(required=False, dump_only=True)
    metadata = fields.Dict(keys=fields.String(), values=fields.String(), required=True)

    directed = fields.Boolean(required=True, validate=validate.Equal(True))

    connection = fields.List(cls_or_instance=ProjectPipelineConnectionField(), required=True)
    compendia = fields.Dict(keys=fields.String(), values=fields.Nested(ProjectPipelineCompendiumSchema()),
                            required=True)


class ProjectPipelineField(ProjectPipelineBase, fields.Field):
    """Marshmallow ProjectPipeline field."""


class ProjectPipelineSchema(ProjectPipelineBase, Schema):
    """Marshmallow ProjectPipeline schema."""


class ProjectPipelineDefinitionMetadata(fields.Field):
    """Marshmallow Pipeline definition metadata schema structure."""
    description = fields.String(required=True)


class ProjectPipelineDefinitionSchema(Schema):
    """Marshmallow ProjectPipelineDefinitionSchema schema."""
    label = fields.String(required=True, load_only=True)
    metadata = ProjectPipelineDefinitionMetadata(required=True, load_only=True)

    graph = ProjectPipelineField(dump_only=True)


class ProjectMultiPipelineSchema(Schema):
    """Marshmallow ProjectMultiGraphGraph schema."""
    pipelines = fields.List(cls_or_instance=ProjectPipelineField(), required=True)


__all__ = (
    "ProjectUserSchema",
    "ProjectMetadataLicensesSchema",
    "ProjectMetadataSchema",
    "ProjectSchema",
    "ProjectPipelineCompendiumSchema",
    "ProjectPipelineConnectionField",
    "ProjectPipelineField",
    "ProjectPipelineSchema",
    "ProjectPipelineDefinitionMetadata",
    "ProjectPipelineDefinitionSchema",
    "ProjectMultiPipelineSchema"
)
