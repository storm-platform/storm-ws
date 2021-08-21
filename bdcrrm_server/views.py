#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Views."""

from bdc_auth_client.decorators import oauth2
from flask import Blueprint, request, jsonify

from .controller import ProjectController
from .forms import ProjectForm

blueprint = Blueprint("bdcrrm", __name__)


@blueprint.route("/project", methods=["POST"])
@oauth2(roles=["admin"])
def create_project(**kwargs):
    """Create a Project."""
    form = ProjectForm()
    project_data = request.get_json()

    errors = form.validate(project_data)
    if errors:
        return errors, 400

    controller = ProjectController()

    user_id = kwargs["user_id"]
    project_object = form.load(project_data)
    project_object["_metadata"] = project_object["metadata"]  # ToDo: Move to a controller layer

    project_created = controller.create_project(user_id, project_object)

    return jsonify(project_created), 201


@blueprint.route("/project", methods=['GET'])
@oauth2()
def list_projects(**kwargs):
    """List all User related projects."""
    controller = ProjectController()
    projects = controller.list_by_user(kwargs["user_id"])

    return jsonify(projects), 200


@blueprint.route("/project/<project_id>", methods=["GET"])
@oauth2()
def get_project_by_user_and_id(**kwarg):
    """Get project by user and project id."""
    controller = ProjectController()
    return controller.get_project_by_id(user_id=kwarg["user_id"], project_id=int(kwarg["project_id"])), 200


@blueprint.route("/project/<project_id>", methods=["DELETE"])
@oauth2()
def delete_project_by_id(**kwarg):
    """Get project by user and project id."""
    controller = ProjectController()
    controller.delete_project_by_id(user_id=kwarg["user_id"], project_id=int(kwarg["project_id"]))

    return {"code": 200, "message": "Project was successfully deleted"}, 200


@blueprint.route("/ping", methods=["GET"])
def ping():
    return {"code": 200, "message": "Pong!"}
