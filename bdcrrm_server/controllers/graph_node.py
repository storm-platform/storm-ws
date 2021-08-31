#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `(Graph) Node Controllers`."""
from ..services.files import BucketService
from ..services.graph_node import ProjectNodeService


class ProjectNodeController:
    """Graph Controller."""

    def create_node(self, user_id: int, project_id: int, node_data):
        service = ProjectNodeService()

        # creating the bucket for the project
        bucket_service = BucketService()
        bucket_id = str(bucket_service.create_bucket().id)

        return service.create_node(user_id=user_id, project_id=project_id, bucket_id=bucket_id, node_data=node_data)

    def get_node(self, user_id: int, project_id: int, node_id: str):
        service = ProjectNodeService()

        # ToDo: Validate data!
        return service.get_node(user_id=user_id, project_id=project_id, node_id=node_id)

    def commit_node(self, user_id: int, project_id: int, node_id: str):
        service = ProjectNodeService()
        return service.commit_node(user_id=user_id, project_id=project_id, node_id=node_id)
