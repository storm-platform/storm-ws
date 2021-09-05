#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Secutiry`."""

from bdc_auth_client.decorators import oauth2
from flask import g
from flask_principal import Identity
from invenio_access import authenticated_user
from invenio_drafts_resources.services.records.permissions import \
    RecordPermissionPolicy
from invenio_records_permissions.generators import AuthenticatedUser


class AuthenticatedUserPermissionPolicy(RecordPermissionPolicy):
    """AuthenticatedUser permission policy. All actions allowed for authenticated users."""

    can_edit = [AuthenticatedUser()]
    can_new_version = [AuthenticatedUser()]
    can_search = [AuthenticatedUser()]
    can_create = [AuthenticatedUser()]
    can_read = [AuthenticatedUser()]
    can_read_draft = [AuthenticatedUser()]
    can_update = [AuthenticatedUser()]
    can_update_draft = [AuthenticatedUser()]
    can_delete = [AuthenticatedUser()]
    can_delete_draft = [AuthenticatedUser()]
    can_publish = [AuthenticatedUser()]
    can_create_files = [AuthenticatedUser()]
    can_read_files = [AuthenticatedUser()]
    can_update_files = [AuthenticatedUser()]
    can_draft_create_files = [AuthenticatedUser()]
    can_draft_read_files = [AuthenticatedUser()]
    can_draft_update_files = [AuthenticatedUser()]
    can_delete_files = [AuthenticatedUser()]


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
        oauth_authenticated_identity = Identity(kwargs.get("user_id", 777))
        oauth_authenticated_identity.provides.add(authenticated_user)

        # `identity` is used by invenio framework services to validate the permissions
        g.identity = oauth_authenticated_identity
        return func(*args, **kwargs)

    return wrapper


__all__ = (
    "authenticate",
    "AuthenticatedUserPermissionPolicy"
)
