#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `File Views`."""

from functools import partial
from urllib.parse import urljoin

from bdc_auth_client.decorators import oauth2
from flask import Blueprint
from invenio_files_rest.models import ObjectVersion, Bucket
from invenio_files_rest.serializer import json_serializer
from invenio_files_rest.views import ObjectResource, BucketResource

from ..forms import ProjectObjectVersionSchema, ProjectBucketSchema
from ..services import ProjectService

GRAPH_NODE_FILES_ENDPOINT = "/graph/<project_id>/node/<node_id>/"


class AuthenticatedResourceMixin:
    """Mixin class for customizing access to arbitrary views.

    This Mixin class customizes arbitrary views with the addition of
    OAuth 2.0 authentication and `bdcrrm` project scope control.
    """

    @oauth2()
    def _oauth_authenticate(self, **kwarg):
        """OAuth 2.0 authentication."""
        return kwarg

    def prepare_project_scope_for_view(self, **kwargs):
        """Authentication and validation of the project scope.

        This function uses the information received from the user for authentication
        and verification of the project scope.
        """
        # authenticating
        oauth_info = self._oauth_authenticate()

        user_id = oauth_info["user_id"]
        project_id = kwargs["project_id"]

        # getting project bucket
        project_service = ProjectService()
        project = project_service.get_project_by_id(user_id, project_id)

        del kwargs["project_id"]
        return dict(
            bucket_id=project.bucket_id,
            **kwargs
        )


class ProjectNodeBucketResource(BucketResource, AuthenticatedResourceMixin):
    """Project Bucket item resource."""

    def get(self, **kwargs):
        """Get list of objects in the bucket."""
        context_descriptor = self.prepare_project_scope_for_view(**kwargs)
        return super(ProjectNodeBucketResource, self).get(**context_descriptor)

    def head(self, **kwargs):
        """Check the existence of the bucket."""
        context_descriptor = self.prepare_project_scope_for_view(**kwargs)
        return super(ProjectNodeBucketResource, self).head(**context_descriptor)


class ProjectNodeObjectResource(ObjectResource, AuthenticatedResourceMixin):
    """Project FileObject item resource."""

    def get(self, **kwargs):
        """Get object or list parts of a multpart upload."""
        context_descriptor = self.prepare_project_scope_for_view(**kwargs)
        return super(ProjectNodeObjectResource, self).get(**context_descriptor)

    def put(self, **kwargs):
        """Update a new object or upload a part of a multipart upload."""
        context_descriptor = self.prepare_project_scope_for_view(**kwargs)
        return super(ProjectNodeObjectResource, self).put(**context_descriptor)

    def delete(self, **kwargs):
        """Delete an object or abort a multipart upload."""
        context_descriptor = self.prepare_project_scope_for_view(**kwargs)
        return super(ProjectNodeObjectResource, self).delete(**context_descriptor)


def invenio_files_rest_blueprint_for_graphnode_files():
    """Create a wrapper blueprint for `Invenio-Files-Rest` views."""

    records_files_blueprint = Blueprint(
        "invenio_records_files", __name__, url_prefix=""
    )

    # defining custom serializer mapping
    custom_serializer_mapping = {
        Bucket: ProjectBucketSchema,
        ObjectVersion: ProjectObjectVersionSchema
    }

    object_view = ProjectNodeObjectResource.as_view("project_node_resource_object_api", serializers={
        'application/json': partial(
            json_serializer,
            view_name="project_node_resource_object_api",
            serializer_mapping=custom_serializer_mapping,
        ),
    })

    bucket_view = ProjectNodeBucketResource.as_view("project_node_resource_bucket_api", serializers={
        'application/json': partial(
            json_serializer,
            view_name="project_node_resource_bucket_api",
            serializer_mapping=custom_serializer_mapping,
        ),
    })

    # add url_rule for `files blueprint` using bdcrrm url schema
    records_files_blueprint.add_url_rule(GRAPH_NODE_FILES_ENDPOINT,
                                         view_func=bucket_view)

    records_files_blueprint.add_url_rule(urljoin(GRAPH_NODE_FILES_ENDPOINT, "<path:key>"),
                                         view_func=object_view)

    return records_files_blueprint
