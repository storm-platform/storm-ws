#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Controllers."""

from typing import Dict, List

import werkzeug.exceptions as http_exceptions

from .forms import ProjectForm
from .models import Project, ProjectUser
from .models import db


class ProjectController:
    """Project Controller."""

    def create_project(self, user_id, data) -> Dict:
        """Create a Project.

        Args:
            user_id (int): Project Owner User ID (from OAuth service)

            data (dict): Project data received from the user.
        Returns:
            Dict: Project created.
        Raises:
            Exception: When Project is not created.
        """
        created_project = None

        with db.session.begin_nested():
            created_project = Project(**data)

            db.session.add(created_project)
            db.session.flush()  # send data to database

            project_user = ProjectUser(
                project_id=created_project.id,
                user_id=user_id,
                is_admin=True,  # 'Owner' is admin
                active=True
            )
            db.session.add(project_user)
        db.session.commit()
        return ProjectForm(exclude=["graph"]).dump(created_project)

    def list_by_user(self, user_id: int) -> List[Project]:
        """List Project by a specific user

        Args:
            user_id (int): Project User ID (from OAuth service)
        Returns:
            List[Project]: List of `user_id` projects.
        """
        user_projects = db.session.query(
            Project
        ).filter(ProjectUser.user_id == user_id).all()

        return [
            ProjectForm(exclude=["graph"]).dump(user_project) for user_project in user_projects
        ] if user_projects else []

    def get_project_by_id(self, user_id: int, project_id: int):
        """Get a project by `user` and `project` id.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            Dict: Project object
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        # ToDo: Fix this metadata transformation
        selected_user.project.metadata = selected_user.project._metadata
        return ProjectForm(exclude=["graph"]).dump(selected_user.project)

    def delete_project_by_id(self, user_id: int, project_id: int):
        """Delete a project object on database.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID that will be deleted.
        Returns:
            Dict: Project object
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        if not selected_user.is_admin:
            raise http_exceptions.Unauthorized(description="Admin access is required to delete a project.")

        with db.session.begin_nested():
            db.session.delete(selected_user.project)
            db.session.delete(selected_user)
        db.session.commit()

    def edit_project_by_id(self, project_id, user_id, project_values):
        """Edit a project object on database.
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        # update the values
        for attr in project_values.keys():
            setattr(selected_user.project, attr, project_values[attr])

        db.session.commit()

        # ToDo: Fix this metadata transformation
        selected_user.project.metadata = selected_user.project._metadata
        return ProjectForm(exclude=["graph"]).dump(selected_user.project)
