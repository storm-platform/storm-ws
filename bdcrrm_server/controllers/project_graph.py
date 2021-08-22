#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Graph Controllers`."""

from typing import Dict

from ..services.project_graph import ProjectGraphService


class ProjectGraphController:
    """Graph Controller."""

    def get_project_graph(self, user_id: int, project_id: int) -> Dict:
        """Get the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            io.BytesIO: The graph file
        """
        controller = ProjectGraphService()
        return controller.get_project_graph(user_id, project_id)

    def delete_project_graph(self, user_id: int, project_id: int) -> None:
        """Delete the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            None: The graph project is removed from database.
        """
        controller = ProjectGraphService()
        controller.delete_project_graph(user_id, project_id)
