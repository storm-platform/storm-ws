#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project resources`."""

from flask import g
from flask_resources import (
    route,
    Resource,
    response_handler,
    resource_requestctx
)

from .adapter import adapter_single_project_graph_as_json, adapter_multi_project_graph_as_json
from ..parser import request_data, request_view_args
from ...schema import (
    ProjectSchema
)
from ...schema.project import ProjectUserSchema


class ProjectResource(Resource):
    """Project resource."""

    def __init__(self, config, service):
        super(ProjectResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        routes = self.config.routes
        return [
            route("GET", routes["list-items"], self.list_project),
            route("POST", routes["create-item"], self.create_project),
            route("GET", routes["get-item"], self.get_project),
            route("PUT", routes["delete-item"], self.edit_project),
            route("DELETE", routes["update-item"], self.delete_project),
            route("POST", routes["create-user"], self.add_user_to_project)
        ]

    @request_data
    @response_handler()
    def create_project(self):
        """Create a new project."""
        project = self.service.create_project(
            g.identity,
            resource_requestctx.data
        )
        return ProjectSchema().dump(project), 201

    @response_handler(many=True)
    def list_project(self):
        """List all project available to the user."""
        user_projects = self.service.list_project_by_user(g.identity)

        form = ProjectSchema()
        return [form.dump(p) for p in user_projects], 200

    @request_view_args
    @response_handler(many=True)
    def get_project(self):
        """Get project by id."""
        user_project = self.service.get_project_by_id(g.identity,
                                                      resource_requestctx.view_args["project_id"])

        return ProjectSchema().dump(user_project), 200

    @request_view_args
    @response_handler()
    def delete_project(self):
        """Delete project."""
        self.service.delete_project_by_id(g.identity, resource_requestctx.view_args["project_id"])

        return {"code": 200, "message": "Project was successfully deleted"}, 200

    @request_data
    @request_view_args
    @response_handler()
    def edit_project(self):
        """Edit project."""
        project_edited = self.service.edit_project_by_id(g.identity,
                                                         resource_requestctx.view_args["project_id"],
                                                         resource_requestctx.data
                                                         )

        return ProjectSchema().dump(project_edited), 200

    @request_view_args
    @response_handler()
    def add_user_to_project(self):
        """Add new user to the project."""
        added_project_user = self.service.add_user_to_project(g.identity,
                                                              resource_requestctx.view_args["user_id"],
                                                              resource_requestctx.view_args["project_id"],
                                                              )

        return ProjectUserSchema().dump(added_project_user), 200


class ProjectGraphResource(Resource):
    """ProjectGraph resource."""

    def __init__(self, config, service):
        super(ProjectGraphResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        """Define resource urls based on configuration routes."""
        routes = self.config.routes
        return [
            route("GET", routes["get-item"], self.get_graph),
            route("GET", routes["list-items"], self.list_graphs),
            route("POST", routes["create-item"], self.create_graph),
            route("DELETE", routes["delete-item"], self.delete_graph)
        ]

    @request_data
    @request_view_args
    @response_handler()
    def create_graph(self):
        """Add a new graph to the project graphs."""
        created_graph = self.service.add_graph(
            g.identity,
            resource_requestctx.view_args["project_id"],
            resource_requestctx.data
        )
        return adapter_single_project_graph_as_json(created_graph), 201

    @request_view_args
    @response_handler()
    def get_graph(self):
        """Add a new graph to the project graphs."""
        selected_graph = self.service.get_graph(
            g.identity,
            resource_requestctx.view_args["project_id"],
            resource_requestctx.view_args["graph_label"],
        )
        return adapter_single_project_graph_as_json(selected_graph), 200

    @request_view_args
    @response_handler()
    def list_graphs(self):
        project_graphs = self.service.list_graph_by_project_id(
            g.identity,
            resource_requestctx.view_args["project_id"],
        )
        return adapter_multi_project_graph_as_json(project_graphs), 200

    @request_view_args
    @response_handler()
    def delete_graph(self):
        """Add a new graph to the project graphs."""
        graph_label = resource_requestctx.view_args["graph_label"]
        self.service.delete_graph(
            g.identity,
            resource_requestctx.view_args["project_id"],
            graph_label
        )
        return {"code": 200, "message": f"Graph ({graph_label}) was successfully deleted"}, 200


class ProjectGraphNodeResource(Resource):
    """ProjectGraphNode resource."""

    def __init__(self, config, service):
        super(ProjectGraphNodeResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        """Define resource urls based on configuration routes."""
        routes = self.config.routes
        return [
            route("POST", routes["create-item"], self.add_node),
            route("DELETE", routes["delete-item"], self.delete_node)
        ]

    @request_view_args
    @response_handler()
    def add_node(self):
        """Add a new node to the project graph."""
        updated_graph = self.service.add_node(
            g.identity,
            resource_requestctx.view_args["project_id"],
            resource_requestctx.view_args["graph_label"],
            resource_requestctx.view_args["node_id"]
        )
        return adapter_single_project_graph_as_json(updated_graph), 201

    @request_view_args
    @response_handler()
    def delete_node(self):
        """Add a new node to the project graph."""
        node_id = resource_requestctx.view_args["node_id"]
        self.service.delete_node(
            g.identity,
            resource_requestctx.view_args["project_id"],
            resource_requestctx.view_args["graph_label"],
            node_id
        )
        return {"code": 200, "message": f"Node {node_id} was successfully deleted"}, 200


__all__ = (
    "ProjectResource",
    "ProjectGraphResource",
    "ProjectGraphNodeResource"
)
