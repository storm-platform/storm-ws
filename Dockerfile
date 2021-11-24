# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-ws is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM inveniosoftware/centos8-python:3.8

#
# Install the storm ws
#
COPY ./ .
RUN python setup.py install
