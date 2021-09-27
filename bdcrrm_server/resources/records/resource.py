#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records resources`."""

from invenio_drafts_resources.resources.records.resource import RecordResource as DraftRecordResourceBase

from invenio_records_resources.resources import RecordResource as RecordResourceBase


class NodeDraftResource(DraftRecordResourceBase):
    ...


class NodeRecordResource(RecordResourceBase):
    ...


__all__ = (
    "NodeDraftResource",
    "NodeRecordResource"
)
