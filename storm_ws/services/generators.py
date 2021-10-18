#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from elasticsearch_dsl import Q

from flask_principal import ItemNeed
from invenio_access import authenticated_user
from invenio_records_permissions.generators import Generator


class ProjectUser(Generator):
    """Allow Project Users."""

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        if record is None:
            return [authenticated_user]

        return [ItemNeed("ispartof", record.parent.project_id, "project")]

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as user project."""
        user_projects = [n.value for n in identity.provides if n.method == "ispartof"]
        if user_projects:
            return Q("terms", **{"parent.project_id": user_projects})


__all__ = (
    "ProjectUser"
)
