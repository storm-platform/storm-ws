#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Server Resources`."""

from flask_resources import Resource, ResourceConfig, route


class ServerResourceConfig(ResourceConfig):
    blueprint_name = "bdcrrm_server"
    url_prefix = "/server"


class ServerResource(Resource):
    """General server resource."""

    def create_url_rules(self):
        return [
            route("GET", "/ping", self.ping)
        ]

    def ping(self):
        """Simple ping-pong to check if the server is running."""
        return {"code": 200, "message": "Pong!"}, 200


__all__ = (
    "ServerResourceConfig",
    "ServerResource"
)
