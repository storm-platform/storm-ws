#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service Extension."""

from invenio_db import InvenioDB
from invenio_search import InvenioSearch
from invenio_access import InvenioAccess
from invenio_records import InvenioRecords
from invenio_files_rest import InvenioFilesREST
from invenio_jsonschemas import InvenioJSONSchemas

from invenio_records_resources import InvenioRecordsResources

from . import config


class StormExt:
    """SpatioTemporal Open Research Manager Web Service Extension."""

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        """Initialize Flask application object."""
        self.init_config(app, **kwargs)
        self.init_invenio_extensions(app, **kwargs)

        app.extensions["storm_ws"] = self

    def init_config(self, app, **kwargs):
        """Initialize configuration."""
        conf = config.get_settings(kwargs["config_name"])
        app.config.from_object(conf)

    def init_invenio_extensions(self, app, **kwargs):
        """Initialize invenio extensions."""
        InvenioDB(app)
        InvenioFilesREST(app)
        InvenioAccess(app)
        InvenioSearch(app)
        InvenioRecords(app)
        InvenioJSONSchemas(app)
        InvenioRecordsResources(app)


__all__ = (
    "StormExt"
)
