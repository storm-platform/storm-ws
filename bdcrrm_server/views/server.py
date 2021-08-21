#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management server views."""

from flask import Blueprint

server_bp = Blueprint("bdcrrm_server", __name__)


@server_bp.route("/ping", methods=["GET"])
def ping():
    return {"code": 200, "message": "Pong!"}, 200
