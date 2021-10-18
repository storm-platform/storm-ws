#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""CLI interface for the SpatioTemporal Open Research Manager Web Service."""

import click
from flask.cli import FlaskGroup

from . import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
@click.version_option()
def cli():
    """Create Flask application."""


if __name__ == '__main__':
    cli()
