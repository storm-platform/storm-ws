#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Resources initializers`."""

import uuid

from storm_ws.services.project.service import UserProfileService

from . import (
    CompendiumFileResource,
    FileCompendiumDraftResourceConfig,
    FileCompendiumRecordResourceConfig,
    CompendiumResource,
    CompendiumResourceConfig,
    ServiceResource,
    ServiceResourceConfig,
    ProjectPipelineResourceConfig,
    ProjectPipelineCompendiumResourceConfig,

    ProjectPipelineResource,
    ProjectPipelineCompendiumResource
)
from .project import (
    ProjectResource,
    ProjectResourceConfig
)
from .server import ServerResourceConfig, ServerResource
from ..services import (
    FileNodeDraftServiceConfig,
    FileNodeRecordServiceConfig,
    CompendiumFileService,
    CompendiumFileDraftService,
    ProjectService,
    ProjectServiceConfig,
    CompendiumServiceConfig,
    CompendiumService,
    ProjectPipelineService,
    ProjectGraphServiceConfig
)


def initialize_project_resources(app) -> None:
    """Initialize the project resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modifications are applied on flask app instance.
    """
    user_profile_service = UserProfileService(None)

    project_service = ProjectService(ProjectServiceConfig, user_profile_service=user_profile_service)
    project_resource = ProjectResource(ProjectResourceConfig, project_service)

    app.register_blueprint(project_resource.as_blueprint())


def initialize_server_resources(app) -> None:
    """Initialize the server resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modifications are applied on flask app instance.
    """
    server_resource = ServerResource(ServerResourceConfig)
    app.register_blueprint(server_resource.as_blueprint())


def initialize_service_resources(app) -> None:
    """Initialize the services resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modifications are applied on flask app instance.
    """
    service_resource = ServiceResource(ServiceResourceConfig)
    app.register_blueprint(service_resource.as_blueprint())


def initialize_pipeline_resources(app) -> None:
    """Initialize the Graph resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modifications are applied on flask app instance.
    """
    # Services
    project_service = ProjectService(ProjectServiceConfig)
    graph_service = ProjectPipelineService(ProjectGraphServiceConfig, project_service)

    # Resources
    graph_resource = ProjectPipelineResource(ProjectPipelineResourceConfig, graph_service)
    graph_node_resource = ProjectPipelineCompendiumResource(ProjectPipelineCompendiumResourceConfig, graph_service)

    # Blueprints
    app.register_blueprint(graph_resource.as_blueprint())
    app.register_blueprint(graph_node_resource.as_blueprint())


def initialize_invenio_records_resources(app) -> None:
    """Initialize the invenio compendium resources.

    Args:
        app (flask.Flask): flask app instance

    Returns:
        None: Modificatios are applied on flask app instance.
    """
    #
    # BDCRRM Project (links all of invenio's modules)
    #
    project_service = ProjectService(ProjectServiceConfig)

    #
    # Files (Draft)
    #
    file_draft_service = CompendiumFileDraftService(FileNodeDraftServiceConfig, project_service=project_service)
    file_draft_resource = CompendiumFileResource(FileCompendiumDraftResourceConfig, file_draft_service)

    #
    # Files (Records)
    #
    file_record_service = CompendiumFileService(FileNodeRecordServiceConfig, project_service=project_service)
    file_record_resource = CompendiumFileResource(FileCompendiumRecordResourceConfig, file_record_service)

    #
    # Nodes
    #
    node_service = CompendiumService(CompendiumServiceConfig, files_service=file_record_service,
                                     draft_files_service=file_draft_service, project_service=project_service)
    node_resource = CompendiumResource(CompendiumResourceConfig, node_service)

    # Files (Draft and Record)
    app.register_blueprint(file_draft_resource.as_blueprint())
    app.register_blueprint(file_record_resource.as_blueprint())

    # Nodes (Draft and Record)
    app.register_blueprint(node_resource.as_blueprint())

    # registry services
    registry = app.extensions["invenio-records-resources"].registry
    registry.register(file_draft_service, str(uuid.uuid4()))
    registry.register(file_record_service, str(uuid.uuid4()))


__all__ = (
    "initialize_pipeline_resources",
    "initialize_server_resources",
    "initialize_project_resources",
    "initialize_service_resources",
    "initialize_invenio_records_resources"
)
