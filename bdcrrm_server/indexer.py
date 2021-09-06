#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Resources`."""
from invenio_indexer.api import RecordIndexer

from .models import NodeDraft, NodeRecord


class DraftDummyIndexer(RecordIndexer):
    record_cls = NodeDraft

    def record_to_index(self, record):
        return 'disabled', 'disabled'

    def index(self, record, arguments=None, **kwargs):
        pass

    def index_by_id(self, record_uuid, **kwargs):
        pass

    def delete(self, record, **kwargs):
        pass


class RecordDummyIndexer(RecordIndexer):
    record_cls = NodeRecord

    def record_to_index(self, record):
        return 'disabled', 'disabled'

    def index(self, record, arguments=None, **kwargs):
        pass

    def index_by_id(self, record_uuid, **kwargs):
        pass

    def delete(self, record, **kwargs):
        pass


__all__ = (
    "DraftDummyIndexer",
    "RecordDummyIndexer"
)
