#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service."""

import os

from flask import Flask, jsonify, request, g

import sqlalchemy.exc as sqlalchemy_exceptions
import werkzeug.exceptions as werkzeug_exceptions
import marshmallow.exceptions as marshmallow_exceptions

from .ext import StormExt

from .config import BaseConfiguration

from .resources.initializer import (
    initialize_pipeline_resources,
    initialize_server_resources,
    initialize_service_resources,
    initialize_project_resources,
    initialize_invenio_records_resources,
)
from .security import authenticate
from .version import __version__


def setup_security_authentication(app):
    """Setup Brazil Data Cube OAuth 2.0 proxy."""

    @app.before_request
    def before_request(**kwargs):
        @authenticate
        def _authenticate(**kwargs):
            pass  # authenticate the user

        # user is able to see the index without access token
        if request.path != "/":
            _authenticate()


def setup_request_proxies(app):
    """Setup proxies that are used to identify the request context (e.g. Project)."""

    @app.before_request
    def project_proxy(**kwargs):
        if request.view_args:
            # Project context
            project_id = request.view_args.get("project_id", None)
            g.project_id = int(project_id) if project_id else project_id

            # Record context
            g.record_id = request.view_args.get("pid_value", None)


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
    @app.after_request
    def after_request(response):
        """Enable CORS."""
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-Api-key")
        return response

    StormExt(app, config_name=config_name)

    # Setup API components
    setup_request_proxies(app)
    setup_exception_handlers(app)
    setup_security_authentication(app)

    # Resources
    initialize_pipeline_resources(app)
    initialize_server_resources(app)
    initialize_project_resources(app)
    initialize_service_resources(app)
    initialize_invenio_records_resources(app)


app = create_app(os.environ.get("STORM_ENVIRONMENT", "DevelopmentConfig"))

__all__ = (
    "__version__",
    "create_app",
)
