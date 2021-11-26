# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-ws is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import jsonify, Blueprint

from .version import __version__


def index():
    """Storm WS index resource."""
    return jsonify(
        dict(
            application_name="SpatioTemporal Open Research Manager", version=__version__
        )
    )


def create_ws_blueprint_api(app):
    """Create Storm WS Index Blueprint."""
    ws_blueprint = Blueprint("storm_ws", __name__)
    ws_blueprint.add_url_rule("/", view_func=index)

    return ws_blueprint


__all__ = "create_ws_blueprint_api"
