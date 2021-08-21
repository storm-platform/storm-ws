#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Marshmallow schemas."""

from marshmallow import Schema, fields


class ProjectMetadataLicensesForm(Schema):
    """Marshmallow project licenses structure."""
    code = fields.String(required=True)
    data = fields.String(required=True)
    text = fields.String(required=True)


class ProjectMetadataForm(Schema):
    """Marshmallow project metadata structure."""
    licenses = fields.Nested(ProjectMetadataLicensesForm, required=True)

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

    metadata = fields.Nested(ProjectMetadataForm, required=True)
