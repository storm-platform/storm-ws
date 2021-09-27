#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Records resources module`."""

from .config import (
    NodeDraftResourceConfig,
    NodeRecordResourceConfig
)

from .resource import (
    NodeDraftResource,
    NodeRecordResource
)

__all__ = (
    "NodeDraftResource",
    "NodeRecordResource",

    "NodeDraftResourceConfig",
    "NodeRecordResourceConfig"
)
