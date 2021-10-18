#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Records resources config`."""

from invenio_drafts_resources.resources import RecordResourceConfig


class NodeResourceConfig(RecordResourceConfig):
    blueprint_name = "node_resources"
    url_prefix = "/graph/<project_id>/node"


__all__ = (
    "NodeResourceConfig"
)
