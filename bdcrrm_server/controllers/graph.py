#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Graph Controllers`."""

from typing import Dict

from ..forms import GraphDocumentForm
from ..services.graph import ProjectGraphService


class ProjectGraphController:
    """Graph Controller."""

    def create_project_graph(self) -> Dict:
        """Create a Project Graph."""
        service = ProjectGraphService()
        return service.create_project_graph()

    def get_project_graph(self, user_id: int, project_id: int) -> Dict:
        """Get the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            io.BytesIO: The graph file
        """
        service = ProjectGraphService()
        selected_project_graph = service.get_project_graph(user_id, project_id)

        return GraphDocumentForm().dump(selected_project_graph.graph)

    def delete_project_graph(self, user_id: int, project_id: int) -> None:
        """Delete the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            None: The graph project is removed from database.
        """
        service = ProjectGraphService()
        service.delete_project_graph(user_id, project_id)

    def clean_project_graph(self, user_id: int, project_id: int) -> None:
        """Clean all nodes from a node.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID that will be deleted.
        Returns:
            None: The graph project is reseted on database.
        """
        service = ProjectGraphService()
        service.clean_project_graph(user_id, project_id)
