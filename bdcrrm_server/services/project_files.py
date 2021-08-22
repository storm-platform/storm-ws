#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `(Graph) Files Services`."""

from invenio_files_rest.models import Bucket

from ..models import db


class BucketService:
    """Files Bucket Service."""

    def create_bucket(self):
        """Create a Bucket.

        Returns:
            Bucket: Created bucket.
        """
        project_bucket = Bucket.create()
        db.session.commit()

        return project_bucket
