#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server ProjectUser models."""

from . import db
from .. import BaseConfiguration


class ProjectUser(db.Model):
    """SQLAlchemy ProjectUser model."""

    __tablename__ = "project_user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    project_id = db.Column(
        db.ForeignKey(f"{BaseConfiguration.BDCRRM_DB_SCHEMA}.project.id", onupdate="CASCADE", ondelete="CASCADE"))

    project = db.relationship("Project", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("user_id", "project_id"),
        dict(schema=BaseConfiguration.BDCRRM_DB_SCHEMA),
    )


__all__ = (
    "ProjectUser"
)
