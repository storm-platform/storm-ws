#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Files Services config`."""

from invenio_records_resources.services import \
    FileServiceConfig as BaseFileServiceConfig

from ...models import NodeDraft, NodeRecord
from ...security import AuthenticatedUserPermissionPolicy


class FileCommonServiceConfig(BaseFileServiceConfig):
    permission_policy_cls = AuthenticatedUserPermissionPolicy


class FileNodeDraftServiceConfig(FileCommonServiceConfig):
    record_cls = NodeDraft


class FileNodeRecordServiceConfig(FileCommonServiceConfig):
    record_cls = NodeRecord
