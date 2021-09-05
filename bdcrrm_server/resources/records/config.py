#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from invenio_drafts_resources.resources import RecordResourceConfig as DraftResourceConfigBase
from invenio_records_resources.resources import RecordResourceConfig as RecordResourceConfigBase


class NodeDraftResourceConfig(DraftResourceConfigBase):
    """Mock record resource configuration."""

    blueprint_name = "node_draft_resources"
    url_prefix = "/graph/<project_id>/node"


class NodeRecordResourceConfig(RecordResourceConfigBase):
    """Mock record resource configuration."""

    blueprint_name = "node_record_resources"
    url_prefix = "/graph/<project_id>/node"
