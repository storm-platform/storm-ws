#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Security module`."""

from flask import g
import werkzeug.exceptions as werkzeug_exceptions

from bdc_auth_client.decorators import oauth2

from invenio_access import authenticated_user
from flask_principal import Identity, Need, ItemNeed

from .services.project.service import UserProfileService


def authenticate(func, **kwargs):
    """Brazil Data Cube OAuth 2.0 authentication client.

    This decorator validates user entries on the Brazil Data Cube OAuth 2.0 service. After
    validation, a `flask_principal.Identity` is defined to use the Invenio Framework functionality.

    Args:
        func (callable): Decorated function

        kwargs (dict): Parameters passed to `bdc_auth_client.decorators.oauth2`.

    Returns:
        callable: Wrapper function.
    """

    @oauth2(**kwargs)
    def wrapper(*args, **kwargs):
        # getting user profile
        user_id = kwargs["user_id"]
        user_profile = UserProfileService(None).get_user_profile_by_id(user_id)

        # creating the base user identity
        user_profile_identity = Identity(user_id)
        user_profile_identity.provides.add(authenticated_user)
        user_profile_identity.provides.add(Need(method="id", value=user_id))

        if not user_profile and g.get("project_id"):  # user has no project and wants to access existing project. Deny!
            raise werkzeug_exceptions.Unauthorized(description="This user is not able to access this project.")

        if user_profile:
            # checking user permission
            if g.get("project_id") and g.project_id not in user_profile.project_ids:
                raise werkzeug_exceptions.Unauthorized(description="This user is not able to access this project.")

            for project_id in user_profile.project_ids:
                user_profile_identity.provides.add(ItemNeed("ispartof", project_id, "project"))

        # `identity` is used by invenio framework services to validate the permissions
        g.identity = user_profile_identity
        return func(*args, **kwargs)

    return wrapper


__all__ = (
    "authenticate"
)
