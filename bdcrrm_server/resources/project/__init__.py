#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project resources module`."""

from .config import (
    ProjectResourceConfig,
    ProjectGraphResourceConfig,
    ProjectGraphNodeResourceConfig
)

from .resource import (
    ProjectResource,
    ProjectGraphResource,
    ProjectGraphNodeResource
)

__all__ = (
    "ProjectResourceConfig",
    "ProjectGraphResourceConfig",
    "ProjectGraphNodeResourceConfig",

    "ProjectResource",
    "ProjectGraphResource",
    "ProjectGraphNodeResource"
)
