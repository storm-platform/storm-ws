#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Project Views."""

from bdc_auth_client.decorators import oauth2
from flask import Blueprint, request, jsonify, send_file

from ..controllers import ProjectController
from ..controllers.project_graph import ProjectGraphController

project_bp = Blueprint("bdcrrm_project", __name__)


@project_bp.route("/project", methods=["POST"])
@oauth2(roles=["admin"])
def create_project(**kwargs):
    """Create a Project."""
    project_data = request.get_json()

    controller = ProjectController()
    project_created = controller.create_project(kwargs["user_id"], project_data)

    return jsonify(project_created), 201


@project_bp.route("/project", methods=['GET'])
@oauth2()
def list_projects(**kwargs):
    """List all User related projects."""
    controller = ProjectController()
    projects = controller.list_by_user(kwargs["user_id"])

    return jsonify(projects), 200


@project_bp.route("/project/<project_id>", methods=["GET"])
@oauth2()
def get_project_by_user_and_id(**kwargs):
    """Get project by user and project id."""
    controller = ProjectController()
    return controller.get_project_by_id(user_id=kwargs["user_id"], project_id=int(kwargs["project_id"])), 200


@project_bp.route("/project/<project_id>", methods=["DELETE"])
@oauth2()
def delete_project_by_id(**kwargs):
    """Delete a project."""
    controller = ProjectController()
    controller.delete_project_by_id(user_id=kwargs["user_id"], project_id=int(kwargs["project_id"]))

    return {"code": 200, "message": "Project was successfully deleted"}, 200


@project_bp.route("/project/<project_id>", methods=["PUT"])
@oauth2()
def edit_project_by_id(**kwargs):
    """Edit a project."""
    project_data = request.get_json()

    controller = ProjectController()
    project_edited = controller.edit_project_by_id(user_id=kwargs["user_id"],
                                                   project_id=int(kwargs["project_id"]),
                                                   attributes_to_chage=project_data)

    return jsonify(project_edited), 200


@project_bp.route("/project/<project_id>/graph", methods=["POST", "PUT"])
@oauth2(roles=["admin"])
def create_or_update_project_graph(**kwargs):
    """Create or update the Project Graph."""
    project_graph = request.files["graph_file"].read()

    controller = ProjectGraphController()
    controller.add_graph_to_project(kwargs["user_id"], kwargs["project_id"], project_graph)

    return {"code": 201, "message": "The graph was successfully added to project"}, 201


@project_bp.route("/project/<project_id>/graph", methods=["GET"])
@oauth2()
def get_project_graph(**kwargs):
    """Create the Project Graph."""
    controller = ProjectGraphController()
    graph_file = controller.get_project_graph(kwargs["user_id"], kwargs["project_id"])

    return send_file(graph_file, mimetype="application/octet-stream", as_attachment=True,
                     attachment_filename="graph"), 200


@project_bp.route("/project/<project_id>/graph", methods=["DELETE"])
@oauth2(roles=["admin"])
def delete_project_graph(**kwargs):
    """Delete the Project Graph."""
    controller = ProjectGraphController()
    controller.delete_project_graph(kwargs["user_id"], kwargs["project_id"])

    return {"code": 200, "message": "The graph was successfully removed from the project"}, 200
