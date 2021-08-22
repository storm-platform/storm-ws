#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Project Models`."""

import datetime

from sqlalchemy.dialects.postgresql import JSONB, UUID

from . import db
from .. import BaseConfiguration


class Project(db.Model):
    """SQLAlchemy Project model."""

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, comment="Project name internally.")
    title = db.Column(db.String(255), nullable=False, comment="A human-readable string naming for project.")
    description = db.Column(db.Text, nullable=True)

    is_public = db.Column(db.Boolean, nullable=False, default=True)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.now)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, )

    graph = db.Column(JSONB, nullable=False, default={})
    _metadata = db.Column("metadata", JSONB, nullable=True, comment="Project metadata.")

    bucket_id = db.Column(UUID, db.ForeignKey("files_bucket.id", onupdate="CASCADE", ondelete="CASCADE"))
    bucket = db.relationship("Bucket", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("name"),
        dict(schema=BaseConfiguration.BDCRRM_DB_SCHEMA),
    )


__all__ = (
    "Project"
)
