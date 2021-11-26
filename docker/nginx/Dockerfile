# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-ws is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM nginx:1.20.2

#
# Nginx config
#
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/* /etc/nginx/conf.d/

#
# Development certificates
#
COPY certs/development.key /etc/ssl/private/test.key
COPY certs/development.crt /etc/ssl/certs/test.crt
