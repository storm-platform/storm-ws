#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""CLI interface for the Brazil Data Cube Reproducible Research Management Server."""

import click
from flask.cli import FlaskGroup

from . import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
@click.version_option()
def cli():
    """Create Flask application."""


if __name__ == '__main__':
    cli()
