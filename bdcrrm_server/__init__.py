#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server."""

import os

from flask import Flask, jsonify

from .version import __version__
from .config import BaseConfiguration
from .views import server_bp, project_bp
from .ext import BDCReproducibleResearchManagement

import sqlalchemy.exc as sqlalchemy_exceptions
import werkzeug.exceptions as werkzeug_exceptions
import marshmallow.exceptions as marshmallow_exceptions

from invenio_files_rest.views import blueprint as invenio_files_rest_bp

from .models import db


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


def setup_exception_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle general exceptions."""
        app.logger.exception(e)
        return {
                   "code": werkzeug_exceptions.InternalServerError.code,
                   "description": werkzeug_exceptions.InternalServerError.description
               }, werkzeug_exceptions.InternalServerError.code

    @app.errorhandler(marshmallow_exceptions.ValidationError)
    def handle_validation_error(e):
        """Handle marshmallow validation exceptions."""
        app.logger.exception(e)
        return jsonify({"code": 400, "message": e.messages}), 400

    @app.errorhandler(sqlalchemy_exceptions.IntegrityError)
    def handle_integrity_value_error(e):
        """Handle database integrity exceptions."""
        app.logger.exception(e)
        return jsonify({"code": 409,
                        "message": "Conflict with resources already in the system. "
                                   "Check the unique identifiers and verify that the "
                                   "resource already exists in the service."}), 409

    @app.errorhandler(werkzeug_exceptions.HTTPException)
    def handle_http_exception_value_error(e):
        """Handle werkzeug.exceptions.HTTPExceptions."""
        app.logger.exception(e)
        return {"code": e.code, "description": e.description}, e.code


def setup_app(app, config_name):
    setup_exception_handlers(app)

    @app.after_request
    def after_request(response):
        """Enable CORS."""
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-Api-key")
        return response

    BDCReproducibleResearchManagement(app, config_name=config_name)

    app.register_blueprint(server_bp)
    app.register_blueprint(project_bp)

    app.register_blueprint(invenio_files_rest_bp)


app = create_app(os.environ.get("BDCRRM_SERVER_ENVIRONMENT", "DevelopmentConfig"))

__all__ = (
    "__version__",
    "create_app",
)
