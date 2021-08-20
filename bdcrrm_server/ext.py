#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server."""

from . import config


class BDCRRM_SERVER:
    """BDCRRM_SERVER extension."""

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        """Initialize Flask application object."""
        self.init_config(app, kwargs)
        app.extensions['bdcrrm_server'] = self

    def init_config(self, app, **kwargs):
        """Initialize configuration."""
        conf = config.get_settings(kwargs['config_name'])

        app.config.from_object(conf)
