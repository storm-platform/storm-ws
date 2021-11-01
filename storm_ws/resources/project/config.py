#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project resources config`."""

from marshmallow import fields
from flask_resources import ResourceConfig


class ProjectResourceConfig(ResourceConfig):
    url_prefix = "/project"
    blueprint_name = "storm_project"

    request_view_args = {"project_id": fields.Str(),
                         "user_id": fields.Int()}

    routes = {
        "list-items": "",
        "create-item": "",
        "get-item": "/<project_id>",
        "delete-item": "/<project_id>",
        "update-item": "/<project_id>",
        "create-user": "/<project_id>/add/user/<user_id>"
    }


class BaseProjectPipelineResourcesConfig(ResourceConfig):
    """Base configurations for Project Pipeline resources."""
    request_view_args = {
        "project_id": fields.Str(),
        "pipeline_label": fields.Str(),
        "compendium_id": fields.Str()
    }


class ProjectPipelineResourceConfig(BaseProjectPipelineResourcesConfig):
    """Pipeline resource config."""

    blueprint_name = "storm_pipeline_resources"
    url_prefix = "/project/<project_id>/pipeline"

    routes = {
        "list-items": "",
        "create-item": "",
        "get-item": "/<pipeline_label>",
        "delete-item": "/<pipeline_label>"
    }


class ProjectPipelineCompendiumResourceConfig(BaseProjectPipelineResourcesConfig):
    """GraphNode resource config."""

    blueprint_name = "storm_pipeline_compendium_resources"
    url_prefix = "/project/<project_id>/pipeline/<pipeline_label>/compendium"

    routes = {
        "create-item": "/<compendium_id>",
        "delete-item": "/<compendium_id>"
    }


__all__ = (
    "ProjectResourceConfig",
    "ProjectPipelineResourceConfig",
    "ProjectPipelineCompendiumResourceConfig"
)
