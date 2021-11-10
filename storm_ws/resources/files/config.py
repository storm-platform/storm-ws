#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Files resources config`."""

from marshmallow import fields
from invenio_records_resources.resources import FileResourceConfig as BaseFileResourceConfig

from ...models import CompendiumDraft, CompendiumRecord


class CompendiumCommonResourceConfig(BaseFileResourceConfig):
    allow_upload = True

    request_view_args = {"pid_value": fields.Str(),
                         "key": fields.Str(),
                         "project_id": fields.Str()}


class FileCompendiumDraftResourceConfig(CompendiumCommonResourceConfig):
    """Custom file resource configuration."""
    record_cls = CompendiumDraft

    blueprint_name = "storm_compendium_draft_files"
    url_prefix = "/pipeline/<project_id>/compendium/<pid_value>/draft"


class FileCompendiumRecordResourceConfig(CompendiumCommonResourceConfig):
    """Custom file resource configuration."""
    record_cls = CompendiumRecord

    blueprint_name = "storm_compendium_record_files"
    url_prefix = "/pipeline/<project_id>/compendium/<pid_value>"


__all__ = (
    "FileCompendiumDraftResourceConfig",
    "FileCompendiumRecordResourceConfig"
)
