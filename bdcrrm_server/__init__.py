#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server."""

import os
import uuid

import marshmallow.exceptions as marshmallow_exceptions
import sqlalchemy.exc as sqlalchemy_exceptions
import werkzeug.exceptions as werkzeug_exceptions
from flask import Flask, jsonify

from .config import BaseConfiguration
from .ext import BDCReproducibleResearchManagement
from .resources import NodeFileResource, FileNodeDraftResourceConfig, FileNodeRecordResourceConfig, NodeDraftResource, \
    NodeDraftResourceConfig, NodeRecordResource, NodeRecordResourceConfig
from .security import authenticate
from .services.files.config import FileNodeDraftServiceConfig, FileNodeRecordServiceConfig
from .services.files.service import NodeFileService
from .services.records.config import NodeDraftServiceConfig, NodeRecordServiceConfig
from .services.records.service import NodeDraftService, NodeRecordService
from .version import __version__
from .views import server_bp, project_bp, graph_bp


def setup_security_authentication(app):
    """Setup Brazil Data Cube OAuth 2.0."""

    @app.before_request
    @authenticate
    def before_request(**kwargs):
        pass


def setup_resources(app):
    #
    # Files (Draft)
    #
    file_draft_service = NodeFileService(FileNodeDraftServiceConfig)
    file_draft_resource = NodeFileResource(FileNodeDraftResourceConfig, file_draft_service)

    #
    # Files (Records)
    #
    file_record_service = NodeFileService(FileNodeRecordServiceConfig)
    file_record_resource = NodeFileResource(FileNodeRecordResourceConfig, file_record_service)

    #
    # Nodes (Draft)
    #
    node_draft_service = NodeDraftService(NodeDraftServiceConfig, files_service=file_record_service,
                                          draft_files_service=file_draft_service)
    node_draft_resource = NodeDraftResource(NodeDraftResourceConfig, node_draft_service)

    #
    # Nodes (Records)
    #
    node_record_service = NodeRecordService(NodeRecordServiceConfig)
    node_record_resource = NodeRecordResource(NodeRecordResourceConfig, node_record_service)

    # Files (Draft and Record)
    app.register_blueprint(file_draft_resource.as_blueprint())
    app.register_blueprint(file_record_resource.as_blueprint())

    # Nodes (Draft and Record)
    app.register_blueprint(node_draft_resource.as_blueprint())
    app.register_blueprint(node_record_resource.as_blueprint())

    # registry services
    registry = app.extensions["invenio-records-resources"].registry
    registry.register(file_draft_service, str(uuid.uuid4()))
    registry.register(file_record_service, str(uuid.uuid4()))


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

    BDCReproducibleResearchManagement(app, config_name=config_name)

    # Old API style (ToDo: refactoring as a Resource)
    app.register_blueprint(graph_bp)
    app.register_blueprint(server_bp)
    app.register_blueprint(project_bp)

    # Setup API components
    setup_exception_handlers(app)
    setup_security_authentication(app)
    setup_resources(app)


app = create_app(os.environ.get("BDCRRM_SERVER_ENVIRONMENT", "DevelopmentConfig"))

__all__ = (
    "__version__",
    "create_app",
)
