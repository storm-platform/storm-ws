#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `ProjectGraph views`."""

from bdc_auth_client.decorators import oauth2
from flask import jsonify

from . import project_bp
from ..controllers.graph import ProjectGraphController


@project_bp.route("/project/<project_id>/graph", methods=["GET"])
@oauth2()
def get_project_graph(**kwargs):
    """Create the Project Graph."""
    controller = ProjectGraphController()
    graph_obj = controller.get_project_graph(kwargs["user_id"], kwargs["project_id"])

    return jsonify(graph_obj), 200


@project_bp.route("/project/<project_id>/graph", methods=["DELETE"])
@oauth2(roles=["admin"])
def delete_project_graph(**kwargs):
    """Delete the Project Graph."""
    controller = ProjectGraphController()
    controller.delete_project_graph(kwargs["user_id"], kwargs["project_id"])

    return {"code": 200, "message": "The graph was successfully removed from the project"}, 200
