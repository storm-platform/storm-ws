#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration options for Brazil Data Cube Reproducible Research Management Server."""

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
                                        "postgresql://bdcrrm-server:bdcrrm-server@localhost:25432/bdcrrm_server")

    BDCRRM_DB_SCHEMA = os.getenv("BDCRRM_DB_SCHEMA", "bdcrrm")


class FlaskConfiguration:
    """Flask Configuration."""
    # Base path used in production (with proxy)
    APPLICATION_ROOT = os.getenv("BDCRRM_SERVER_PREFIX", "/")
    SESSION_COOKIE_PATH = os.getenv("SESSION_COOKIE_PATH", "/")


class BaseConfiguration(FlaskConfiguration, DatabaseConfiguration, OAuthConfiguration):
    """Base Configuration."""
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'secret-key'


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
