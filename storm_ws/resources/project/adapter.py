#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project resources response adapters`."""

from typing import Dict, List

from ...models import ProjectPipeline
from ...schema import ProjectPipelineSchema, ProjectMultiPipelineSchema


def _get_pipeline_from_project(project_pipeline: ProjectPipeline) -> Dict:
    """Get the Graph object from ProjectPipeline object.

    Args:
        project_pipeline (ProjectPipeline): ProjectPipeline object.
    Returns:
        Dict: Pipeline retrieved from ProjectPipeline.
    """
    pipeline_obj = project_pipeline.pipeline
    return pipeline_obj.get("pipeline") if "pipeline" in pipeline_obj else pipeline_obj


def adapter_single_project_pipeline_as_json(project_pipeline: ProjectPipeline) -> Dict:
    """Adapt a single ProjectGraph to a JSON format.

    Args:
        project_pipeline (ProjectGraph): ProjectGraph object.

    Returns:
        Dict: adapted pipeline object.
    """
    return dict(
        pipeline=ProjectPipeline().dump(dict(
            label=project_pipeline.label,
            **_get_pipeline_from_project(project_pipeline)
        ))
    )


def adapter_multi_project_pipeline_as_json(project_pipelines: List[ProjectPipeline]) -> Dict:
    """Adapt a multiple Project Pipeline to a JSON format.

    Args:
        project_pipelines (List[ProjectPipeline]): List of Project Pipelines.

    Returns:
        Dict: adapted pipeline object.
    """
    pipeline_schema = ProjectPipelineSchema()
    return ProjectMultiPipelineSchema().dump(
        dict(graphs=[
            dict(
                dict(
                    label=p.label
                ),
                **pipeline_schema.dump(_get_pipeline_from_project(p))
            ) for p in project_pipelines
        ]
        )
    )


__all__ = (
    "adapter_multi_project_pipeline_as_json",
    "adapter_single_project_pipeline_as_json"
)
