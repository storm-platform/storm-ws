#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `(Graph) Files Services`."""
from invenio_files_rest.models import Bucket
from invenio_records_resources.services import FileServiceConfig as BaseFileServiceConfig
from invenio_records_resources.services.files.components import FileMetadataComponent, FileContentComponent

from bdcrrm_server.services.components import BaseServiceComponentized
from ..models import db, NodeDraft


class BucketService:
    """Files Bucket Service."""

    def create_bucket(self, **kwargs):
        """Create a Bucket.

        Returns:
            Bucket: Created bucket.
        """
        project_bucket = Bucket.create(**kwargs)
        db.session.commit()

        return project_bucket


class DraftFileServiceConfig(BaseFileServiceConfig):
    """File service configuration."""

    components = [
        FileMetadataComponent,
        FileContentComponent
    ]


class NodeRecordFileService(BaseServiceComponentized):
    """Node Records Files Service."""
    record_cls = NodeDraft

    def get_record(self, id_):
        return self.record_cls.pid.resolve(id_, registered_only=False)

    def init_files(self, id_, data):
        record = self.get_record(id_)

        # ToDo: Verificar qual component possui esse comportamento
        self.run_components("init_files", id_, None, record, data)

        db.session.commit()

        # ToDo: Verificar qual component possui esse comportamento
        self.run_components("post_init_files", id_, None, record, data)

        # ToDo: Adicionar um retorno que seja o suficiente para as views e que se
        #       adeque ao serviço do bdcrrm-server
        return record.dumps()

    def set_file_content(self, id_, file_key, stream, content_length=None):
        record = self.get_record(id_)

        # ToDo: Verificar qual component possui esse comportamento
        self.run_components("set_file_content", id_, file_key, None, stream, content_length, record)
        db.session.commit()

        # ToDo: Verificar qual component possui esse comportamento
        self.run_components("post_set_file_content", id_, file_key, None, stream, content_length, record)

        # ToDo: Adicionar um retorno que seja o suficiente para as views e que se
        #       adeque ao serviço do bdcrrm-server
        return record.dumps()

    def commit_file(self, id_, file_key):
        """Commit a file upload."""
        record = self.get_record(id_)

        # ToDo: Verificar qual component possui esse comportamento
        self.run_components("commit_file", id_, file_key, None, record)

        db.session.commit()

        # ToDo: Verificar qual component possui esse comportamento
        self.run_components("post_commit_file", id_, file_key, None, record)

        # ToDo: Adicionar um retorno que seja o suficiente para as views e que se
        #       adeque ao serviço do bdcrrm-server
        return record.dumps()
