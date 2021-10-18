#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
FROM inveniosoftware/centos8-python:3.8

#
# Install the storm ws
#
COPY ./ .
RUN python setup.py install
