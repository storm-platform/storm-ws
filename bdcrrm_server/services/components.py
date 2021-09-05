#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Services Componentized`."""
from invenio_drafts_resources.services.records.components import ServiceComponent


class NodeRecordServiceComponent(ServiceComponent):

    def create(self, identity, data=None, record=None, errors=None):
        super().create(identity, data=None, record=None, errors=None)

        # Data files
        datafiles = data.get("data", {})
        record.inputs = datafiles.get("inputs", [])
        record.outputs = datafiles.get("outputs", [])

        # Environment
        record.environment = data.get("environment", {})

        # Commands
        record.command = data.get("command")
        record.command_checksum = data.get("command_checksum")
