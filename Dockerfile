#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
FROM inveniosoftware/centos8-python:3.8

#
# Install the bdcrrm-server
#
COPY ./ .
RUN python setup.py install
