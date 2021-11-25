# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-ws is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SpatioTemporal Open Research Manager Web Service Extension."""

from . import config


class StormWS:
    """SpatioTemporal Open Research Manager Web Service Extension."""

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        """Initialize Flask application object."""
        self.init_config(app)

        app.extensions["storm_ws"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            app.config.setdefault(k, getattr(config, k))


__all__ = "StormWS"
