#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project services config`."""

from ...security import AuthenticatedUserPermissionPolicy


class ProjectServiceConfig:
    permission_policy_cls = AuthenticatedUserPermissionPolicy


class ProjectGraphServiceConfig:
    permission_policy_cls = AuthenticatedUserPermissionPolicy


__all__ = (
    "ProjectServiceConfig",
    "ProjectGraphServiceConfig"
)
