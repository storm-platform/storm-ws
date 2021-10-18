#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Service Resources`."""

from flask_resources import Resource, ResourceConfig, route


class ServiceResourceConfig(ResourceConfig):
    blueprint_name = "storm_service"
    url_prefix = ""


class ServiceResource(Resource):
    """General service resource."""

    def create_url_rules(self):
        return [
            route("GET", "/", self.index)
        ]

    def index(self):
        """Simple ping-pong to check if the server is running."""
        return {"application_name": "SpatioTemporal Open Research Manager Web Service", "version": "0.1"}, 200


__all__ = (
    "ServiceResourceConfig",
    "ServiceResource"
)
