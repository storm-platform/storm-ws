#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Marshmallow schemas."""

from flask import request, url_for
from invenio_files_rest.serializer import BucketSchema, ObjectVersionSchema
from marshmallow import Schema, fields, validate, post_dump


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

    graph = fields.Raw(required=False)
    metadata = fields.Nested(ProjectMetadataForm(), required=True)

    bucket_id = fields.UUID(required=True, load_only=True)


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
    label = fields.String(required=True)
    metadata = fields.Nested(GraphNodeMetadata(), required=True)


class GraphEdgeForm(fields.Field):
    """Marshamllow Graph Edge structure."""
    source = fields.String(required=True)
    target = fields.String(required=True)


class GraphForm(Schema):
    """Marshmallow Project Graph structure."""
    directed = fields.Boolean(required=True, validate=validate.Equal(True))
    nodes = fields.Dict(keys=fields.String(), values=fields.Nested(GraphNodeForm()))
    edges = fields.List(cls_or_instance=GraphEdgeForm())


class GraphDocumentForm(Schema):
    """Marshmallow Project Graph structure."""
    graph = fields.Nested(GraphForm)


class ProjectObjectVersionSchema(ObjectVersionSchema):
    """Invenio Schema for ProjectObjectVersionSchema (bdcrrm.Project + invenio.ObjectVersion)."""

    def dump_links(self, o):
        """Dump links."""
        project_id = request.view_args["project_id"]
        url_path = ".{0}".format(self.context.get("view_name"))
        params = {"versionId": o.version_id}

        url_for_self = url_for(
            url_path,
            project_id=project_id,
            key=o.key,
            _external=True,
            **(params if not o.is_head or o.deleted else {})
        )
        url_for_versions = url_for(
            url_path, project_id=project_id, key=o.key, _external=True, **params
        )

        data = {"self": url_for_self, "version": url_for_versions}

        if o.is_head and not o.deleted:
            url_for_uploads = "{0}?uploads".format(
                url_for(
                    url_path, project_id=project_id, key=o.key, _external=True
                )
            )
            data.update({"uploads": url_for_uploads})

        return data

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        """Wrap response in envelope."""
        if not many:
            return data
        else:
            data = {"contents": data}
            bucket = self.context.get("bucket")
            if bucket:
                data.update(
                    ProjectBucketSchema(context=self.context).dump(bucket).data
                )
            return data


class ProjectBucketSchema(BucketSchema):
    """Invenio Schema for ProjectBucketSchema (bdcrrm.Project + invenio.Bucket)."""

    def dump_links(self, o):
        """Dump links."""
        project_id = request.view_args["project_id"]

        url_path = ".{0}".format(self.context.get("view_name"))
        url_for_self = url_for(url_path, project_id=project_id, _external=True)

        url_for_versions = "{0}?versions".format(url_for_self)
        url_for_uploads = "{0}?uploads".format(url_for_self)

        return {
            "self": url_for_self,
            "versions": url_for_versions,
            "uploads": url_for_uploads,
        }
