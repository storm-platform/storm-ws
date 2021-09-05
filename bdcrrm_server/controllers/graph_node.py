# #
# # This file is part of Brazil Data Cube Reproducible Research Management Server.
# # Copyright (C) 2021 INPE.
# #
# # Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# # under the terms of the MIT License; see LICENSE file for more details.
# #
#
# """Brazil Data Cube Reproducible Research Management Server `(Graph) Node Controllers`."""
# from typing import Dict
#
# from ..services.files import BucketService
# from ..services.graph_node import ProjectNodeService, ProjectNodeDraftService
#
#
# class ProjectNodeDraftController:
#     """Node Draft controller."""
#
#     def create_node_draft(self, user_id: int, project_id: int, node_draft_data: Dict):
#         """"""
#
#         node_draft_service = ProjectNodeDraftService(BucketService())
#         return node_draft_service.create_node_draft(user_id, project_id, node_draft_data)
#
#
# class ProjectNodeController:
#     """Graph Controller."""
#
#     def create_node(self, user_id: int, project_id: int, node_data):
#         """ToDo"""
#         # creating the bucket for the project
#         # bucket_service = BucketService()
#         # bucket_id = str(bucket_service.create_bucket().id)
#
#         # node_service = ProjectNodeService(BucketService())
#         # return node_service.create_node(user_id=user_id, project_id=project_id, node_data=node_data)
#         # user_id: int, project_id: int is temporary disabled!
#         return None  # node_service.create_node(node_data=node_data)
#
#     def get_node(self, user_id: int, project_id: int, node_id: str):
#         service = ProjectNodeService()
#
#         # ToDo: Validate data!
#         return service.get_node(user_id=user_id, project_id=project_id, node_id=node_id)
#
#     def commit_node(self, user_id: int, project_id: int, node_id: str):
#         service = ProjectNodeService()
#         return service.commit_node(user_id=user_id, project_id=project_id, node_id=node_id)
