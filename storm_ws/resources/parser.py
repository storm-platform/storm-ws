#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `parsers for Flask Resources`."""

from flask_resources import request_body_parser, from_conf, request_parser

request_data = request_body_parser(
    parsers=from_conf("request_body_parsers"),
    default_content_type=from_conf("default_content_type")
)

request_view_args = request_parser(
    from_conf("request_view_args"), location="view_args"
)

__all__ = (
    "request_data",
    "request_view_args"
)
