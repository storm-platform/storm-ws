#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `ProjectGraphNode views`."""

from bdc_auth_client.decorators import oauth2
from flask import jsonify, request

from . import graph_bp
from ..controllers.graph_node import ProjectNodeController


# Pedir sugestão:
# /project/<project_id>/graph/node/<node_id>/files

# ou (separar as entidades em duas rotas)
# /graph/<project_id>/node
# /graph/<project_id>/node/files

@graph_bp.route("/graph/<project_id>/node", methods=["GET"])
@oauth2()
def get_project_graph_nodes(**kwargs):
    """Create a graph node."""
    graph_node_data = request.get_json()

    controller = ProjectNodeController()
    node_created = controller.create_node(kwargs["user_id"], kwargs["project_id"], graph_node_data)

    # ToDo: Adicionar marshmallow form!
    return jsonify({"node_id": node_created.node_id}), 200


@graph_bp.route("/graph/<project_id>/node", methods=["POST"])
@oauth2()
def create_project_graph_node(**kwargs):
    """Create a graph node."""
    graph_node_data = request.get_json()

    controller = ProjectNodeController()
    node_created = controller.create_node(kwargs["user_id"], kwargs["project_id"], graph_node_data)

    # ToDo: Adicionar marshmallow form!
    return jsonify({"node_id": node_created.node_id}), 200


@graph_bp.route("/graph/<project_id>/<node_id>", methods=["GET"])
@oauth2()
def get_project_graph_node(**kwargs):
    """Get a specific graph node."""

    controller = ProjectNodeController()
    selected_node = controller.get_node(kwargs["user_id"], kwargs["project_id"], kwargs["node_id"])

    # ToDo: Adicionar marshmallow form!
    return jsonify({"node_id": selected_node.node_id}), 200


@graph_bp.route("/graph/<project_id>/<node_id>/commit", methods=["GET"])
@oauth2()
def commit_project_graph_node_draft(**kwargs):
    """Get a specific graph node."""

    controller = ProjectNodeController()
    selected_node = controller.commit_node(kwargs["user_id"], kwargs["project_id"], kwargs["node_id"])

    # ToDo: Adicionar marshmallow form!
    return jsonify({"node_id": selected_node.node_id}), 200
