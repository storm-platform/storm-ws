#
# This file is part of Brazil Data Cube Reproducible Research Management Server.
# Copyright (C) 2021 INPE.
#
# Brazil Data Cube Reproducible Research Management Server is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Brazil Data Cube Reproducible Research Management Server `Services Componentized`."""


class BaseServiceComponentized:

    def __init__(self, config):
        """Constructor.

        Args:
            config (object): Service configuration object
        """
        self.config = config

    @property
    def components(self):
        return (c(self) for c in self.config.components)

    def run_components(self, operation, *args, **kwargs):
        """Run components fro a given operation."""

        for component in self.components:
            if hasattr(component, operation):
                getattr(component, operation)(*args, **kwargs)
