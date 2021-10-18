#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Cache configurations`."""

from cacheout import CacheManager

cache_manager = CacheManager({
    "users_profile": {
        "maxsize": 512,
        "ttl": 3600
    }
})

__all__ = (
    "cache_manager"
)
