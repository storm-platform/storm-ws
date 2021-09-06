#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project Resources`."""

from flask import g
from flask_resources import Resource, ResourceConfig, route, request_body_parser, from_conf, response_handler, \
    resource_requestctx, request_parser
from marshmallow import fields

from bdcrrm_server.forms import ProjectForm

request_data = request_body_parser(
    parsers=from_conf("request_body_parsers"),
    default_content_type=from_conf("default_content_type")
)

request_view_args = request_parser(
    from_conf("request_view_args"), location="view_args"
)


class ProjectResourceConfig(ResourceConfig):
    blueprint_name = "bdcrrm_project"
    url_prefix = "/project"

    request_view_args = {"project_id": fields.Str()}


class ProjectResource(Resource):
    """Project resource."""

    def __init__(self, config, service):
        super(ProjectResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        return [
            route("GET", "", self.list_project),
            route("POST", "", self.create_project),
            route("GET", "/<project_id>", self.get_project),
            route("PUT", "/<project_id>", self.edit_project),
            route("DELETE", "/<project_id>", self.delete_project)
        ]

    @request_data
    @response_handler()
    def create_project(self):
        """Create a new project."""
        project = self.service.create_project(
            g.identity,
            resource_requestctx.data
        )
        return ProjectForm().dump(project), 201

    @response_handler(many=True)
    def list_project(self):
        """List all project available to the user."""
        user_projects = self.service.list_project_by_user(g.identity)

        form = ProjectForm()
        return [form.dump(p) for p in user_projects], 200

    @request_view_args
    @response_handler(many=True)
    def get_project(self):
        """Get project by id."""
        user_project = self.service.get_project_by_id(g.identity,
                                                      resource_requestctx.view_args["project_id"])

        return ProjectForm().dump(user_project), 200

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

        return ProjectForm().dump(project_edited), 201


__all__ = (
    "ProjectResourceConfig",
    "ProjectResource"
)
