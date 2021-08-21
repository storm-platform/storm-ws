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
from invenio_files_rest.views import blueprint as invenio_files_rest_bp
from werkzeug.exceptions import HTTPException, InternalServerError

from .config import BaseConfiguration
from .ext import BDCReproducibleResearchManagement
from .version import __version__
from .views import blueprint as bdcrrm_bp


def create_app(config_name='DevelopmentConfig'):
    """Create the Flask application from a given config object type.
    Args:
        config_name (string): Config instance name.
    Returns:
        Flask Application with config instance scope.
    """
    app = Flask(__name__)

    with app.app_context():
        setup_app(app, config_name)

        return app


def setup_app(app, config_name):
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle exceptions."""
        if isinstance(e, HTTPException):
            return {'code': e.code, 'description': e.description}, e.code

        app.logger.exception(e)

        return {'code': InternalServerError.code,
                'description': InternalServerError.description}, InternalServerError.code

    @app.after_request
    def after_request(response):
        """Enable CORS."""
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-Api-key")
        return response

    BDCReproducibleResearchManagement(app, config_name=config_name)

    app.register_blueprint(bdcrrm_bp)
    app.register_blueprint(invenio_files_rest_bp)


app = create_app(os.environ.get("BDCRRM_SERVER_ENVIRONMENT", "DevelopmentConfig"))

__all__ = (
    "__version__",
    "create_app",
)
