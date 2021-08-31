#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project Services`."""

from typing import Dict

import werkzeug.exceptions as werkzeug_exceptions

from ..models import ProjectUser
from ..models import db


class ProjectGraphService:
    """Project Graph Service."""

    def get_project_graph(self, user_id: int, project_id: int) -> Dict:
        """Get the Graph associated to a Project.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            Dict: JSON Graph document
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        if selected_user.project.graph is None:
            raise werkzeug_exceptions.NotFound(description="There is no graph associated with the Project.")

        return selected_user.project.graph

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

        if selected_user.project.graph is None:
            raise werkzeug_exceptions.NotFound(description="There is no graph associated with the Project.")

        selected_user.project.graph = {}
        db.session.add(selected_user.project)
        db.session.commit()
