# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-ws is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM inveniosoftware/centos8-python:3.8

#
# App dependencies
#
COPY pyproject.toml poetry.lock ./
RUN pip3 install pip wheel setuptools --upgrade \
    && pip3 install poetry \
    # Configuring the poetry to install the dependencies
    # in the system site package
    && poetry config virtualenvs.create false \
    && poetry install

#
# Project related files
#
COPY ./docker/uwsgi/ ${INVENIO_INSTANCE_PATH}
COPY ./invenio.cfg ${INVENIO_INSTANCE_PATH}
COPY ./ .

#
# Entrypoint
#
ENTRYPOINT [ "bash", "-c" ]
