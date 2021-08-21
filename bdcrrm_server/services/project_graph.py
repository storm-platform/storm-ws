#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Project Services."""

import io

from ..models import ProjectUser
from ..models import db

import werkzeug.exceptions as werkzeug_exceptions


class ProjectGraphService:
    """Project Grapg Service."""

    def add_graph_to_project(self, user_id: int, project_id: int, graph_file: bytes) -> None:
        """Add graph to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID

            graph_file (bytes): file bytes
        Returns:
            None: The file will be added to project record on database.
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        if not selected_user.is_admin:
            raise werkzeug_exceptions.Unauthorized(
                description="Admin access is required to directly modify the graph project.")

        if selected_user.project.graph:
            raise werkzeug_exceptions.Conflict(description="There is already a graph associated with the Project.")

        project = selected_user.project
        project.graph = graph_file

        db.session.add(project)
        db.session.commit()

    def get_project_graph(self, user_id: int, project_id: int) -> io.BytesIO:
        """Get the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            io.BytesIO: The graph file
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        if not selected_user.project.graph:
            raise werkzeug_exceptions.NotFound(description="There is no graph associated with the Project.")

        return io.BytesIO(selected_user.project.graph)

    def delete_project_graph(self, user_id: int, project_id: int) -> None:
        """Delete the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            None: The graph project is removed from database.
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        if not selected_user.is_admin:
            raise werkzeug_exceptions.Unauthorized(description="Admin access is required to delete the Project.")

        if not selected_user.project.graph:
            raise werkzeug_exceptions.NotFound(description="There is no graph associated with the Project.")

        selected_user.project.graph = None
        db.session.add(selected_user.project)
        db.session.commit()
