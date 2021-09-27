#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `parsers for flask-resources`."""

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
