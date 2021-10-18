#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project Models`."""

import datetime

from sqlalchemy import UniqueConstraint

from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from .. import db
from ..base import BaseModel
from ...config import BaseConfiguration


#
# Database models
#

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

    _metadata = db.Column("metadata", JSONB, nullable=True, comment="Project metadata.")

    __table_args__ = (
        db.UniqueConstraint("name"),
        dict(schema=BaseConfiguration.STORM_DB_SCHEMA),
    )


class ProjectUser(db.Model):
    """SQLAlchemy ProjectUser model."""

    __tablename__ = "project_user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    project_id = db.Column(
        db.ForeignKey(f"{BaseConfiguration.STORM_DB_SCHEMA}.project.id", onupdate="CASCADE", ondelete="CASCADE"))

    project = db.relationship("Project", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("user_id", "project_id"),
        dict(schema=BaseConfiguration.STORM_DB_SCHEMA),
    )


class ProjectGraph(db.Model):
    """SQLAlchemy ProjectGraph model."""

    __tablename__ = "project_graph"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    graph = db.Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=False)
    label = db.Column(db.String(40), nullable=False, comment="Graph identification label.")

    project_id = db.Column(
        db.ForeignKey(f"{BaseConfiguration.STORM_DB_SCHEMA}.project.id", onupdate="CASCADE", ), nullable=False)
    project = db.relationship("Project", lazy="joined")

    __table_args__ = (
                         UniqueConstraint("project_id", "label", name="project_graph_labels"),
                     ) + BaseModel.__table_args__


__all__ = (
    "Project",
    "ProjectUser",
    "ProjectGraph"
)
