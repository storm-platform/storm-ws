#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Endpoint links`."""

from copy import deepcopy

from flask import g, request
from invenio_records_resources.services import Link, FileLink
from invenio_records_resources.services.base.links import preprocess_vars


class NodeRecordLink(Link):
    """Short cut for writing Node Record links."""

    @staticmethod
    def vars(record, vars):
        """Variables for the URI template."""
        vars.update({
            "id": record.pid.pid_value,
            "project_id": record.parent.project_id or g.project_id,
            "args": {
                "access_token": request.args.get("access_token", )
            }
        })


class PaginationNodeRecordLink(Link):
    """Short cut for writing Node Record links."""

    def expand(self, obj, context):
        """Expand the URI Template."""
        context = {"project_id": g.project_id, **context}

        vars = {}
        vars.update(deepcopy(context))
        self.vars(obj, vars)
        if self._vars_func:
            self._vars_func(obj, vars)
        vars = preprocess_vars(vars)
        return self._uritemplate.expand(**vars)


class NodeFileLink(FileLink):
    """Short cut for writing record links."""

    @staticmethod
    def vars(file_record, vars):
        """Variables for the URI template."""
        vars.update({
            "key": file_record.key,
            "project_id": g.project_id,
            "args": {
                "access_token": request.args.get("access_token", )
            }
        })


def node_pagination_links(tpl):
    """Create pagination links (prev/selv/next) from the same template."""
    return {
        "prev": PaginationNodeRecordLink(
            tpl,
            when=lambda pagination, ctx: pagination.has_prev,
            vars=lambda pagination, vars: vars["args"].update({
                "page": pagination.prev_page.page
            })
        ),
        "self": PaginationNodeRecordLink(tpl),
        "next": PaginationNodeRecordLink(
            tpl,
            when=lambda pagination, ctx: pagination.has_next,
            vars=lambda pagination, vars: vars["args"].update({
                "page": pagination.next_page.page
            })
        ),
    }


__all__ = (
    "NodeFileLink",
    "NodeRecordLink",

    "node_pagination_links"
)
