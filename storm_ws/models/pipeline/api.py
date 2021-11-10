#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Graph API`."""

from werkzeug.local import LocalProxy

from invenio_drafts_resources.records import Draft, Record

from invenio_pidstore.models import PIDStatus
from invenio_records.dumpers import ElasticsearchDumper
from invenio_rdm_records.records.systemfields import HasDraftCheckField

from invenio_records_resources.records.api import FileRecord

from invenio_records.systemfields import (
    ModelField,
    DictField,
    ConstantField
)

from invenio_records_resources.records.systemfields import (
    PIDStatusCheckField,
    FilesField,
    IndexField
)

from .models import (
    CompendiumParentMetadata,
    CompendiumVersionsState,
    CompendiumFileDraftMetadata,
    CompendiumDraftMetadata,
    CompendiumFileRecordMetadata,
    CompendiumRecordMetadata
)

from invenio_drafts_resources.records.api import ParentRecord as ParentRecordBase


class CompendiumParent(ParentRecordBase):
    """Node Parent record."""

    model_cls = CompendiumParentMetadata

    project_id = ModelField(dump=True)
    project = ModelField(dump=False)

    dumper = ElasticsearchDumper()

    schema = ConstantField(
        "$schema", "local://records/compendiumparent-v1.0.0.json"
    )


class CommonFieldsMixin:
    """Common system fields between compendium records and drafts."""

    versions_model_cls = CompendiumVersionsState
    parent_record_cls = CompendiumParent

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)

    inputs = DictField("data.inputs")
    outputs = DictField("data.outputs")

    environment = DictField("environment")

    command = DictField("command")
    command_checksum = DictField("command_checksum")

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)
    pids = DictField("pids")

    dumper = ElasticsearchDumper()
    schema = ConstantField(
        '$schema', 'local://records/compendiumrecord-v1.0.0.json')


class CompendiumFileDraft(FileRecord):
    model_cls = CompendiumFileDraftMetadata
    record_cls = LocalProxy(lambda: CompendiumDraft)


class CompendiumDraft(CommonFieldsMixin, Draft):
    model_cls = CompendiumDraftMetadata

    index = IndexField("compendium_records-drafts-compendiumdraft-v1.0.0", search_alias="compendium_records")

    files = FilesField(
        store=False,
        file_cls=CompendiumFileDraft,
        delete=False
    )

    has_draft = HasDraftCheckField()


class CompendiumFileRecord(FileRecord):
    model_cls = CompendiumFileRecordMetadata
    record_cls = LocalProxy(lambda: CompendiumRecord)


class CompendiumRecord(CommonFieldsMixin, Record):
    model_cls = CompendiumRecordMetadata

    index = IndexField("compendium_records-records-compendiumrecord-v1.0.0", search_alias="compendium_records-records")

    files = FilesField(
        store=False,
        file_cls=CompendiumFileRecord,
        create=False,
        delete=False
    )

    has_draft = HasDraftCheckField(CompendiumDraft)


__all__ = (
    "CompendiumParent",
    "CompendiumDraft",
    "CompendiumFileDraft",
    "CompendiumRecord",
    "CompendiumFileRecord"
)
