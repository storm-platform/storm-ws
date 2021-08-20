#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server."""

import os

from flask import Flask

from .ext import BDCRRM_SERVER
from .version import __version__


def create_app(config_name='DevelopmentConfig'):
    """Create the Flask application from a given config object type.

    Args:
        config_name (string): Config instance name.

    Returns:
        Flask Application with config instance scope.
    """
    app = Flask(__name__)

    BDCRRM_SERVER(app, config_name=config_name)

    return app


app = create_app(os.environ.get('BDCRRM_SERVER_ENVIRONMENT', 'DevelopmentConfig'))

__all__ = (
    '__version__',
    'create_app',
)
