#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project Services`."""

from typing import Dict, List

import werkzeug.exceptions as werkzeug_exceptions

from ..models import Project, ProjectUser
from ..models import db


class ProjectService:
    """Project Service."""

    def create_project(self, user_id, data) -> Dict:
        """Create a Project.

        Args:
            user_id (int): Project Owner User ID (from OAuth service)

            data (dict): Project data received from the user.
        Returns:
            Project: Created Project Object.
        Raises:
            Exception: When Project is not created.
        """
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
        return created_project

    def list_project_by_user(self, user_id: int) -> List[Project]:
        """List Project by a specific user

        Args:
            user_id (int): Project User ID (from OAuth service)
        Returns:
            List[Project]: List of `user_id` projects.
        """
        return db.session.query(
            Project
        ).filter(ProjectUser.user_id == user_id).all()

    def get_project_by_id(self, user_id: int, project_id: int) -> Project:
        """Get a project by `user` and `project` id.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            Project: List of Project object
        """
        user_projects = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        return user_projects.project

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
            raise werkzeug_exceptions.Unauthorized(description="Admin access is required to delete the project.")

        with db.session.begin_nested():
            db.session.delete(selected_user.project)
            db.session.delete(selected_user)
        db.session.commit()

    def edit_project_by_id(self, project_id, user_id, attributes_to_chage: Dict) -> Project:
        """Edit a project object on database.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID that will be deleted.

            attributes_to_chage (Dict): Attributes (and values) that will be changed on database record.
        Returns:
            Project: The project updated on the database.
        """
        selected_user = db.session.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == user_id
        ).first_or_404("Project not found!")

        if not selected_user.is_admin:
            raise werkzeug_exceptions.Unauthorized(description="Admin access is required to edit the project.")

        # update the values
        for attr in attributes_to_chage.keys():
            setattr(selected_user.project, attr, attributes_to_chage[attr])

        db.session.commit()
        return selected_user.project
