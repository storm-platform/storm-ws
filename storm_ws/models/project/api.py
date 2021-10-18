#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from typing import List


#
# User API
#
class UserProfile:

    def __init__(self, id: int, project_ids: List[int]):
        self._id = id
        self._project_ids = project_ids

    @property
    def id(self) -> int:
        return self._id

    @property
    def project_ids(self) -> List[int]:
        return self._project_ids


__all__ = (
    "UserProfile"
)
