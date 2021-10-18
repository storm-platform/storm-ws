#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project services`."""

from typing import Dict, List

from copy import deepcopy

import werkzeug.exceptions as werkzeug_exceptions
from bdcrrm_api.graph import (
    JSONGraphConverter,
    ExecutionGraphManager
)
from invenio_records_resources.services import Service

from ..cache import cache_manager
from ...models import Project, ProjectGraph, NodeRecord
from ...models import ProjectUser, UserProfile
from ...models import db
from ...schema import (
    ProjectGraphDefinitionSchema
)
from ...schema import ProjectSchema


class UserProfileService(Service):
    """UserProfile Service."""

    def get_user_profile_by_id(self, user_id) -> UserProfile:
        """Select User profile by id.

        Args:
            user_id (int): User id (from OAuth service)

        Returns:
            UserProfile: User profile selected.
        """
        user_data = cache_manager["users_profile"].get(user_id)

        if not user_data:
            user_data = db.session.query(ProjectUser).filter(
                ProjectUser.user_id == user_id
            )

            # validating the data
            if user_data.count() == 0:
                return None

            # retrieving data and remove disabled projects
            user_data = user_data.all()
            user_data = list(filter(lambda x: x.active, user_data))

            # saving all project ids
            project_ids = list(map(lambda x: x.project_id, user_data))

            user_data = UserProfile(user_id, project_ids)
            cache_manager["users_profile"].set(user_id, user_data)
        return user_data

    def flush_user_profile(self, user_id):
        """Flush loaded user profile from cache (if exists).

        Args:
            user_id (int): User id (from OAuth service)

        Returns:
            None: User profile is flushed in-place.
        """
        cache_manager["users_profile"].delete(user_id)


class ProjectService(Service):
    """Project Service."""

    def __init__(self, config, user_profile_service=None):
        """Initializer for NodeDraftRecordService."""
        super(ProjectService, self).__init__(config)
        self._user_profile_service = user_profile_service

    def _get_project_user_by_project_id(self, identity, project_id):
        """Select ProjectUser by Project.

        Args:
            identity (flask_principal.Identity): Project Owner User ID (from OAuth service)

            project_id (int): Project ID

        Returns:
            ProjectUser: Selected ProjectUser

        Raises:
            Exception: when the project is not found.
        """
        return db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == identity.id
        ).first_or_404("Project not found!")

    def create_project(self, identity, data) -> Dict:
        """Create a Project.

        Args:
            identity (flask_principal.Identity): Project Owner User ID (from OAuth service)

            data (dict): Project data received from the user.
        Returns:
            Project: Created Project Object.
        Raises:
            Exception: When Project is not created.
        """
        # validating
        form = ProjectSchema()
        form.load(data)

        data["_metadata"] = data["metadata"]

        with db.session.begin_nested():
            created_project = Project(**data)

            db.session.add(created_project)
            db.session.flush()  # send data to database

            project_user = ProjectUser(
                project_id=created_project.id,
                user_id=identity.id,
                is_admin=True,  # 'Owner' is admin
                active=True
            )
            db.session.add(project_user)
        db.session.commit()

        # flushing previous loaded user profile
        self._user_profile_service.flush_user_profile(identity.id)
        return created_project

    def list_project_by_user(self, identity) -> List[Project]:
        """List Project by a specific user

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)
        Returns:
            List[Project]: List of `user_id` projects.
        """
        return db.session.query(
            Project
        ).filter(ProjectUser.user_id == identity.id).all()

    def get_project_by_id(self, identity, project_id: int) -> Project:
        """Get a project by `user` and `project` id.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID
        Returns:
            Project: List of Project object
        """
        return self._get_project_user_by_project_id(identity, project_id).project

    def delete_project_by_id(self, identity, project_id: int):
        """Delete a project object on database.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID that will be deleted.
        Returns:
            Dict: Project object
        """
        selected_user = self._get_project_user_by_project_id(identity, project_id)

        if not selected_user.is_admin:
            raise werkzeug_exceptions.Unauthorized(description="Admin access is required to delete the project.")

        with db.session.begin_nested():
            db.session.delete(selected_user.project)
            db.session.delete(selected_user)
        db.session.commit()

    def edit_project_by_id(self, identity, project_id, attributes_to_chage: Dict) -> Project:
        """Edit a project object on database.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID that will be deleted.

            attributes_to_chage (Dict): Attributes (and values) that will be changed on database record.
        Returns:
            Project: The project updated on the database.
        """
        # validating
        form = ProjectSchema()
        form.load(attributes_to_chage, partial=True)

        selected_user = self._get_project_user_by_project_id(identity, project_id)

        if not selected_user.is_admin:
            raise werkzeug_exceptions.Unauthorized(description="Admin access is required to edit the project.")

        # update the values
        for attr in attributes_to_chage.keys():
            setattr(selected_user.project, attr, attributes_to_chage[attr])

        db.session.commit()
        return selected_user.project

    def add_user_to_project(self, identity, user_id, project_id):
        """Add user to a project.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            user_id (int): User identity (from OAuth service) that will be added on project.

            project_id (int): Project ID that will be deleted.
        Returns:
            Dict: Project object
        """
        selected_user = self._get_project_user_by_project_id(identity, project_id)

        if not selected_user.is_admin:
            raise werkzeug_exceptions.Unauthorized(description="Admin access is required to delete the project.")

        project_user = ProjectUser(
            project_id=project_id,
            user_id=user_id,
            is_admin=False,
            active=True
        )
        db.session.add(project_user)
        db.session.commit()

        # flushing previous loaded user profile
        self._user_profile_service.flush_user_profile(user_id)
        return project_user


class ProjectGraphService(Service):
    """Graph Service."""

    def __init__(self, config, project_service=None):
        """Constructor for GraphService."""
        super().__init__(config)
        self._project_service = project_service

    def add_graph(self, identity, project_id: int, data) -> Dict:
        """Add a new graph to the project.

        Args:
            identity (flask_principal.Identity): Project Owner User ID (from OAuth service)

            project_id (int): Project ID

            data (dict): Graph data received from the user.
        Returns:
            Project: Created Graph Object.
        Raises:
            Exception: When Graph is not created.
        """
        # validating
        form = ProjectGraphDefinitionSchema()
        form.load(data)

        # populate the graph with the another information
        data = dict(
            label=data["label"],
            graph=dict(
                edges=[],
                nodes={},
                directed=True,
                type="Execution Graph",
                metadata=data["metadata"]
            )
        )

        # search for the project linked to the graph
        project = self._project_service.get_project_by_id(identity, project_id)
        data["project_id"] = project.id  # avoiding unauthorized registers

        created_project_graph = ProjectGraph(**data)

        db.session.add(created_project_graph)
        db.session.commit()

        return created_project_graph

    def get_graph(self, identity, project_id: int, project_graph_label: str) -> ProjectGraph:
        """Get a specific Graph by `project` and `graph` id.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID

            project_graph_label (str): Project graph identification
        Returns:
            ProjectGraph: Project graph
        """
        return db.session.query(ProjectGraph).filter(
            ProjectGraph.project_id == project_id,
            ProjectGraph.label == project_graph_label
        ).first_or_404("Graph not found!")

    def list_graph_by_project_id(self, identity, project_id: int = None) -> List[ProjectGraph]:
        """Get a Graph by `user` and `project` id.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID
        Returns:
            List[ProjectGraph]: List of Graph object
        """
        return db.session.query(ProjectGraph).filter(
            ProjectGraph.project_id == project_id
        ).all()

    def add_node(self, identity, project_id: int, project_graph_label: str, node_id: str) -> ProjectGraph:
        """Add a new node to the Project Graph.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID

            project_graph_label (str): Project graph identification

            node_id (str): NodeRecord ID that will be added.

        Returns:
            ProjectGraph: Project graph created.
        """
        selected_graph = self.get_graph(identity, project_id, project_graph_label)

        selected_node_record = NodeRecord.pid.resolve(node_id)
        if not selected_node_record.is_published:
            raise werkzeug_exceptions.BadRequest(description="NodeRecord must be published to be used as a GraphNode")

        # adding the selected node to the graph
        selected_execution_graph = deepcopy(selected_graph.graph)
        graph_manager = ExecutionGraphManager(JSONGraphConverter.from_json({"graph": selected_execution_graph}))

        graph_command = selected_node_record.command
        graph_repropack = selected_node_record.environment["key"]
        graph_inputs = [x["key"] for x in selected_node_record["data"]["inputs"]]
        graph_outputs = [x["key"] for x in selected_node_record["data"]["outputs"]]

        # introducing checksum verification
        graph_inputs = [selected_node_record.files[file_name].file.file_model.checksum for file_name in graph_inputs]
        graph_outputs = [selected_node_record.files[file_name].file.file_model.checksum for file_name in graph_outputs]

        graph_manager.add_vertex(graph_repropack, graph_command, graph_inputs, graph_outputs, name=node_id)

        # saving the changed graph
        selected_graph.graph = JSONGraphConverter.to_json(graph_manager.graph, attribute_as_index="name").get("graph")

        db.session.add(selected_graph)
        db.session.commit()

        return selected_graph

    def delete_node(self, identity, project_id: int, project_graph_label: str, node_id: str) -> None:
        """Delete a node from the Project Graph.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID

            project_graph_label (str): Project graph identification

            node_id (str): NodeRecord ID that will be added.

        Returns:
            ProjectGraph: Project graph created.
        """
        selected_graph = self.get_graph(identity, project_id, project_graph_label)

        # adding the selected node to the graph
        graph_manager = ExecutionGraphManager(JSONGraphConverter.from_json({"graph": selected_graph.graph}))

        # searching for the vertex that will be deleted
        if graph_manager.graph.vs:
            selected_node = graph_manager.graph.vs.select(name=node_id)

            if selected_node:
                graph_manager.delete_vertex(
                    " ".join(["".join(x.split()) for x in selected_node["command"][0].split("  ")]))

                selected_graph.graph = (
                    JSONGraphConverter.to_json(graph_manager.graph, attribute_as_index="name")
                        .get("graph")
                )
                db.session.add(selected_graph)
                db.session.commit()

                return
        raise werkzeug_exceptions.NotFound(description=f"{node_id} not found!")

    def delete_graph(self, identity, project_id: int, project_graph_label: str) -> None:
        """Delete a ProjectGraph.

        Args:
            identity (flask_principal.Identity): Project User identity (from OAuth service)

            project_id (int): Project ID

            project_graph_label (str): Project graph identification
        Returns:
            ProjectGraph: Project graph
        """
        selected_graph = self.get_graph(identity, project_id, project_graph_label)

        db.session.delete(selected_graph)
        db.session.commit()


__all__ = (
    "ProjectService",
    "UserProfileService",
    "ProjectGraphService"
)