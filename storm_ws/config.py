#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration options for SpatioTemporal Open Research Manager Web Service."""

import os


def get_settings(env):
    """Get the given enviroment configuration."""
    return CONFIG.get(env)


class OAuthConfiguration:
    """OAuth Configuration."""
    BDC_AUTH_CLIENT_ID = os.getenv("BDC_AUTH_CLIENT_ID", None)
    BDC_AUTH_CLIENT_SECRET = os.getenv("BDC_AUTH_CLIENT_SECRET", None)
    BDC_AUTH_ACCESS_TOKEN_URL = os.getenv("BDC_AUTH_ACCESS_TOKEN_URL", None)


class DatabaseConfiguration:
    """Database Configuration."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgresql://storm:storm@localhost:5432/storm-db")

    STORM_DB_SCHEMA = os.getenv("STORM_DB_SCHEMA", "storm_ws")


class FlaskConfiguration:
    """Flask Configuration."""
    # Base path used in production (with proxy)
    APPLICATION_ROOT = os.getenv("STORM_SERVER_PREFIX", "/")
    SESSION_COOKIE_PATH = os.getenv("SESSION_COOKIE_PATH", "/")


class SearchEngineConfiguration:
    """OpenSearch/Elasticsearch Configuration.

    See:
        More details are available on invenio-search documentation: https://invenio-search.readthedocs.io/en/latest/
    """
    SEARCH_ENGINE_DEFAULT_CONFIGURATION = dict(
        port=9200,
        scheme="http",
        host='localhost'
    )

    SEARCH_CLIENT_CONFIG = dict(
        hosts=[
            SEARCH_ENGINE_DEFAULT_CONFIGURATION
        ]
    )


class InvenioJSONSchemaAPIConfigurations:
    """Invenio JSONSchema Configurations.

    See:
        More details are available on module repository: https://github.com/inveniosoftware/invenio-jsonschemas
    """
    JSONSCHEMAS_HOST = "local"  # avoiding warning

    RECORDS_REFRESOLVER_CLS = "invenio_records.resolver.InvenioRefResolver"
    RECORDS_REFRESOLVER_STORE = "invenio_jsonschemas.proxies.current_refresolver_store"


class BaseConfiguration(FlaskConfiguration, DatabaseConfiguration, OAuthConfiguration, SearchEngineConfiguration,
                        InvenioJSONSchemaAPIConfigurations):
    """Base Configuration."""
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'secret-key'

    #
    # Invenio settings
    #
    SITE_UI_URL = os.environ.get("SITE_UI_URL", None)
    SITE_API_URL = os.environ.get("SITE_API_URL", None)


class ProductionConfiguration(BaseConfiguration):
    """Production Mode."""


class DevelopmentConfiguration(BaseConfiguration):
    """Development Mode."""
    DEVELOPMENT = True


class TestingConfiguration(BaseConfiguration):
    """Testing Mode (Continous Integration)."""

    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfiguration(),
    "ProductionConfig": ProductionConfiguration(),
    "TestingConfig": TestingConfiguration()
}
