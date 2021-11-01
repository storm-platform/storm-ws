#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Records resources config`."""

from invenio_drafts_resources.resources import RecordResourceConfig


class CompendiumResourceConfig(RecordResourceConfig):
    blueprint_name = "storm_compendium_resources"
    url_prefix = "/pipeline/<project_id>/compendium"


__all__ = (
    "CompendiumResourceConfig"
)
