#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Base model`."""

from ..config import BaseConfiguration


class BaseModel:
    __table_args__ = (
        dict(schema=BaseConfiguration.BDCRRM_DB_SCHEMA),
    )
