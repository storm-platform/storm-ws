#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Views."""

from flask import Blueprint

graph_bp = Blueprint("bdcrrm_graph", __name__, )
server_bp = Blueprint("bdcrrm_server", __name__)
project_bp = Blueprint("bdcrrm_project", __name__)

from .server import ping

from .project import *

from .graph import *
from .graph_node import *

__all__ = (
    "project_bp",
    "server_bp"
)
