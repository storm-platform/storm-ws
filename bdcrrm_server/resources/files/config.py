#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_records_resources.resources import FileResourceConfig as BaseFileResourceConfig
from marshmallow import fields

from ...models import NodeDraft, NodeRecord


class NodeCommonResourceConfig(BaseFileResourceConfig):
    allow_upload = True

    request_view_args = {"pid_value": fields.Str(),
                         "key": fields.Str(),
                         "project_id": fields.Str()}


class FileNodeDraftResourceConfig(NodeCommonResourceConfig):
    """Custom file resource configuration."""
    record_cls = NodeDraft

    blueprint_name = "node_draft_files"
    url_prefix = "/graph/<project_id>/node/<pid_value>/draft"


class FileNodeRecordResourceConfig(NodeCommonResourceConfig):
    """Custom file resource configuration."""
    record_cls = NodeRecord

    blueprint_name = "node_record_files"
    url_prefix = "/graph/<project_id>/node/<pid_value>"
