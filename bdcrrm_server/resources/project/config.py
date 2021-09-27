#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project resources config`."""

from flask_resources import ResourceConfig
from marshmallow import fields


class ProjectResourceConfig(ResourceConfig):
    url_prefix = "/project"
    blueprint_name = "bdcrrm_project"

    request_view_args = {"project_id": fields.Str()}

    routes = {
        "list-items": "",
        "create-item": "",
        "get-item": "/<project_id>",
        "delete-item": "/<project_id>",
        "update-item": "/<project_id>"
    }


class BaseProjectGraphResourcesConfig(ResourceConfig):
    """Base configurations for Project Graph resources."""
    request_view_args = {
        "project_id": fields.Str(),
        "graph_label": fields.Str(),
        "node_id": fields.Str()
    }


class ProjectGraphResourceConfig(BaseProjectGraphResourcesConfig):
    """Graph resource config."""

    blueprint_name = "graph_resources"
    url_prefix = "/project/<project_id>/graph"

    routes = {
        "list-items": "",
        "create-item": "",
        "get-item": "/<graph_label>",
        "delete-item": "/<graph_label>"
    }


class ProjectGraphNodeResourceConfig(BaseProjectGraphResourcesConfig):
    """GraphNode resource config."""

    blueprint_name = "graph_node_resources"
    url_prefix = "/project/<project_id>/graph/<graph_label>/node"

    routes = {
        "create-item": "/<node_id>",
        "delete-item": "/<node_id>"
    }


__all__ = (
    "ProjectResourceConfig",
    "ProjectGraphResourceConfig",
    "ProjectGraphNodeResourceConfig"
)
