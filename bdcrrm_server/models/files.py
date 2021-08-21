#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server Files models."""

from invenio_files_rest.models import ObjectVersion

from . import db
from .. import BaseConfiguration


class ProjectObjectVersion(ObjectVersion):
    """Specialized SQLAlchemy ObjectVersion model.

    Note:
        `ObjectVersion` is a concept introduced by invenio-files-rest. For more information,
        see the documentation page: https://invenio-files-rest.readthedocs.io/en/latest/overview.html
    """
    project_id = db.Column(
        db.Integer, db.ForeignKey(f"{BaseConfiguration.BDCRRM_DB_SCHEMA}.project.id"), nullable=False)


__all__ = (
    "ProjectObjectVersion"
)
