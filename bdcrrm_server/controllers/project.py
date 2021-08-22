#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project Controllers`."""

from typing import Dict, List

from ..forms import ProjectForm
from ..services import ProjectService
from ..services.project_files import BucketService


def _fix_metadata(project):
    """Fix `_metadata` field."""
    project.metadata = project._metadata
    return project


class ProjectController:
    """Project Controller."""

    def create_project(self, user_id: int, data: Dict) -> Dict:
        """Create a Project."""
        # validating
        form = ProjectForm(exclude=["graph", "bucket_id"])
        form.load(data)
        data["_metadata"] = data["metadata"]

        # creating the bucket for the project
        bucket_service = BucketService()
        data["bucket_id"] = str(bucket_service.create_bucket().id)

        # creating the project
        service = ProjectService()
        created_project = service.create_project(user_id, data)

        return form.dump(created_project)

    def list_by_user(self, user_id: int) -> List[Dict]:
        """List Project by a specific user

        Args:
            user_id (int): Project User ID (from OAuth service)
        Returns:
            List[Project]: List of `user_id` projects.
        """
        service = ProjectService()
        user_projects = service.list_project_by_user(user_id)

        form = ProjectForm(exclude=["graph"])
        return [form.dump(_fix_metadata(p)) for p in user_projects]

    def get_project_by_id(self, user_id: int, project_id: int):
        """Get a project by `user` and `project` id.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID
        Returns:
            Dict: Project object
        """
        service = ProjectService()
        user_project = service.get_project_by_id(user_id, project_id)

        return ProjectForm(exclude=["graph"]).dump(_fix_metadata(user_project))

    def delete_project_by_id(self, user_id: int, project_id: int):
        """Delete a project object on database.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID that will be deleted.
        Returns:
            Dict: Project object
        """
        service = ProjectService()
        service.delete_project_by_id(user_id, project_id)

    def edit_project_by_id(self, project_id, user_id, attributes_to_chage: Dict) -> Dict:
        """Edit a project object on database.

        Args:
            user_id (int): Project User ID (from OAuth service)

            project_id (int): Project ID that will be deleted.

            attributes_to_chage (Dict): Attributes (and values) that will be changed on database record.
        Returns:
            Dict: The project updated on database.
        """
        # validating
        form = ProjectForm(exclude=["graph"])
        form.load(attributes_to_chage, partial=True)

        service = ProjectService()
        edited_project = service.edit_project_by_id(project_id, user_id, attributes_to_chage)

        return ProjectForm(exclude=["graph"]).dump(_fix_metadata(edited_project))
