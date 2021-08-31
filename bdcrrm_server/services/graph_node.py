#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project Services`."""

from typing import Dict

import base32_lib as base32

from ..models import ProjectUser
from ..models import db


class ProjectNodeService:
    """Project Node Service."""

    def create_node(self, user_id: int, project_id: int, bucket_id: str, node_data: Dict): ...

    def get_node(self, user_id: int, project_id: int, node_id: str): ...

    def commit_node(self, user_id, project_id, node_id): ...


### ToDo: Remover o conteúdo abaixo (Deixado somente como rascunho)
#
#     # ToDo: Alterar para create_draft_node
#     def create_node(self, user_id: int, project_id: int, bucket_id: str, node_data: Dict):
#         selected_user = db.session.query(ProjectUser).filter(
#             ProjectUser.project_id == project_id,
#             ProjectUser.user_id == user_id
#         ).first_or_404("Project not found!")
#
#         # ToDo: Check permission (can user perform this action on the selected project ?)
#         # selected_user
#
#         # Creating node id
#         node_id = base32.generate(length=10, split_every=5, checksum=True)
#
#         # saving
#         # ToDo: O `node_id` já vem do cliente gerado!
#         created_project = ProjectNodeDraft(node_id=node_id, node_metadata=node_data, bucket_id=bucket_id,
#                                            project_id=project_id)
#
#         db.session.add(created_project)
#         db.session.commit()
#         return created_project
#
#     def get_node(self, user_id: int, project_id: int, node_id: str):
#         selected_node = db.session.query(ProjectNodeDraft).filter(
#             ProjectNodeDraft.project_id == project_id,
#             ProjectNodeDraft.node_id == node_id
#         ).first_or_404("NodeID not found!")
#
#         # ToDo: Na hora de devolver os dados, é importante que os recursos do nó, armazenados no serviço
#         # sejam associados com seus devidos links! isso facilita para o cliente utilizar o serviço e principalmente
#         # para montar um grafo partindo de resultados já calculados!
#
#         # ToDo: Validate
#         # ToDo: Create marshmallow form for GraphNode
#         return selected_node
#
#         # ToDo: Add validations here!
#         # selected_user = db.session.query(ProjectUser).filter(
#         #     ProjectUser.project_id == project_id,
#         #     ProjectUser.user_id == user_id
#         # ).first_or_404("Project not found!")
#
#     def commit_node(self, user_id, project_id, node_id):
#         selected_node = db.session.query(ProjectNodeDraft).filter(
#             ProjectNodeDraft.project_id == project_id,
#             ProjectNodeDraft.node_id == node_id
#         ).first_or_404("Graph Node not found!")
#
#         # Para a realização do commit, algumas etapas são necessárias:
#
#         # 1° Validação dos arquivos enviados (ToDo)
#         # Consultar o bucket e verificar se todos os arquivos de declarados, de fato, estão disponíveis
#
#         # 2° Montar o novo grafo e validar as propriedades gerais (Não sei, se da para montar o grafo,
#         # algo nesse sentido. Ou mesmo se ele tem alguma inconsistência do tipo e etc) (ToDo).
#         # ToDo: Fazer o build do grafo
#         # ToDo: Aplicar a operação de rebuild de nós
#
#         # 2.1. Carregar o nó no grafo
#         # 2.2. Adicionar o novo nó ao grafo
#
#         # 3° Salvar o grafo alterado
#
#         # 4° Excluir o registro de draft
#         with db.session.begin_nested():
#             db.session.delete(selected_node)
#         db.session.commit()
#
#
# '''
# subgraph -> subgraph.id
#
# {
#
# }
# '''
#
# # My Invenio Implementation
# # from invenio_drafts_resources.services.records import RecordService
# from invenio_records_resources.services import RecordService as base
#
#
# # class NodeRecordService(base):
# #     ...
# #
# #
# # a = NodeRecordService()
# # a.search_drafts()
#
# from ..models.my_invenio_models import NodeDraftMetadata
