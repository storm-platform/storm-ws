#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records resources config`."""

from invenio_drafts_resources.resources import RecordResourceConfig


class NodeResourceConfig(RecordResourceConfig):
    blueprint_name = "node_resources"
    url_prefix = "/graph/<project_id>/node"


__all__ = (
    "NodeResourceConfig"
)
