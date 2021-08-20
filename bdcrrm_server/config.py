#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration options for Brazil Data Cube Reproducible Research Management Server."""

import os

_BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_settings(env):
    """Get the given enviroment configuration."""
    return CONFIG.get(env)

class Config:
    """Base Configuration."""

    DEBUG = False
    TESTING = False

    SECRET_KEY = 'secret-key'

    BDCRRM_SERVER_BASE_PATH_TEMPLATES = os.getenv('BDCRRM_SERVER_BASE_PATH_TEMPLATES', 'templates')

    BDCRRM_SERVER_SMTP_PORT = os.getenv('BDCRRM_SERVER_SMTP_PORT', 587)
    BDCRRM_SERVER_SMTP_HOST = os.getenv('BDCRRM_SERVER_SMTP_HOST', None)

    BDCRRM_SERVER_EMAIL_ADDRESS = os.getenv('BDCRRM_SERVER_EMAIL_ADDRESS', None)
    BDCRRM_SERVER_EMAIL_PASSWORD = os.getenv('BDCRRM_SERVER_EMAIL_PASSWORD', None)

    BDCRRM_SERVER_APM_APP_NAME = os.environ.get('BDC_AUTH_APM_APP_NAME', None)
    BDCRRM_SERVER_APM_HOST = os.environ.get('BDC_AUTH_APM_HOST', None)
    BDCRRM_SERVER_APM_SECRET_TOKEN = os.environ.get('BDC_AUTH_APM_SECRET_TOKEN', None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/bdcrrm_server')

    OAUTH2_REFRESH_TOKEN_GENERATOR = True

    # Default OAuth 2.0 client app for Brazil Data Cube
    BDCRRM_SERVER_DEFAULT_APP = 'bdc-auth'

    # Base path used in production (with proxy)
    APPLICATION_ROOT = os.getenv('BDCRRM_SERVER_PREFIX', '/')
    SESSION_COOKIE_PATH = os.getenv('SESSION_COOKIE_PATH', '/')

    # Logstash configuration
    BDC_LOGSTASH_URL = os.getenv('BDC_LOGSTASH_URL', 'localhost')
    BDC_LOGSTASH_PORT = os.getenv('BDC_LOGSTASH_PORT', 5044)


class ProductionConfig(Config):
    """Production Mode."""


class DevelopmentConfig(Config):
    """Development Mode."""

    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)."""

    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}