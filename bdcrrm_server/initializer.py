#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Resources initializers`."""

import uuid

from .resources import NodeFileResource, FileNodeDraftResourceConfig, FileNodeRecordResourceConfig, NodeDraftResource, \
    NodeDraftResourceConfig, NodeRecordResource, NodeRecordResourceConfig
from .resources.server import ServerResourceConfig, ServerResource
from .services.files.config import FileNodeDraftServiceConfig, FileNodeRecordServiceConfig
from .services.files.service import NodeFileService
from .services.records.config import NodeDraftServiceConfig, NodeRecordServiceConfig
from .services.records.service import NodeDraftService, NodeRecordService


def initialize_server_resources(app) -> None:
    """Initialize the server resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modificatios are applied on flask app instance.
    """
    server_resource = ServerResource(ServerResourceConfig)
    app.register_blueprint(server_resource.as_blueprint())


def initialize_invenio_records_resources(app) -> None:
    """Initialize the invenio records resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modificatios are applied on flask app instance.
    """
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


__all__ = (
    "initialize_server_resources",
    "initialize_invenio_records_resources"
)
