#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Endpoint links`."""

from flask import g, request
from invenio_records_resources.services import Link, FileLink


class NodeRecordLink(Link):
    """Short cut for writing Node Record links."""

    @staticmethod
    def vars(record, vars):
        """Variables for the URI template."""
        vars.update({
            "id": record.pid.pid_value,
            "project_id": record.parent.project_id or g.project_id,  # for bdcrrm application
            "args": {
                "access_token": request.args.get("access_token", )  # required for bdcrrm applications
            }
        })


class NodeFileLink(FileLink):
    """Short cut for writing record links."""

    @staticmethod
    def vars(file_record, vars):
        """Variables for the URI template."""
        vars.update({
            "key": file_record.key,
            "project_id": file_record.record.parent.project_id,
            "args": {
                "access_token": request.args.get("access_token", )
            }
        })


__all__ = (
    "NodeRecordLink",
    "NodeFileLink"
)
