#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Files services config`."""

from invenio_records_resources.services import FileServiceConfig as BaseFileServiceConfig

from ..components import (
    ProjectValidatorFileServiceComponent,
    NodeDraftFileDefinitionValidatorComponent
)
from ...models import NodeDraft, NodeRecord
from ...security import AuthenticatedUserPermissionPolicy


class FileCommonServiceConfig(BaseFileServiceConfig):
    permission_policy_cls = AuthenticatedUserPermissionPolicy

    components = BaseFileServiceConfig.components + [
        ProjectValidatorFileServiceComponent
    ]


class FileNodeDraftServiceConfig(FileCommonServiceConfig):
    record_cls = NodeDraft

    components = FileCommonServiceConfig.components + [
        NodeDraftFileDefinitionValidatorComponent,
    ]


class FileNodeRecordServiceConfig(FileCommonServiceConfig):
    record_cls = NodeRecord


__all__ = (
    "FileCommonServiceConfig",
    "FileNodeDraftServiceConfig",
    "FileNodeRecordServiceConfig"
)
