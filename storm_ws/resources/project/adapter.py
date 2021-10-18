#
# This file is part of SpatioTemporal Open Research Manager Web Service.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager Web Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager Web Service `Project resources response adapters`."""

from typing import Dict, List

from ...models import ProjectGraph
from ...schema import ProjectGraphSchema, ProjectMultiGraphSchema


def _get_graph_from_project(project_graph: ProjectGraph) -> Dict:
    """Get the Graph object from ProjectGraph object.

    Args:
        project_graph (ProjectGraph): ProjectGraph object.
    Returns:
        Dict: Graph retrieved from ProjectGraph.
    """
    graph_obj = project_graph.graph
    return graph_obj.get("graph") if "graph" in graph_obj else graph_obj


def adapter_single_project_graph_as_json(project_graph: ProjectGraph) -> Dict:
    """Adapt a single ProjectGraph to a JSON format.

    Args:
        project_graph (ProjectGraph): ProjectGraph object.

    Returns:
        Dict: adapted graph object.
    """
    return dict(
        graph=ProjectGraphSchema().dump(dict(
            label=project_graph.label,
            **_get_graph_from_project(project_graph)
        ))
    )


def adapter_multi_project_graph_as_json(project_graphs: List[ProjectGraph]) -> Dict:
    """Adapt a multiple ProjectGraph to a JSON format.

    Args:
        project_graph (List[ProjectGraph]): ProjectGraph object.

    Returns:
        Dict: adapted graph object.
    """
    graph_schema = ProjectGraphSchema()
    return ProjectMultiGraphSchema().dump(
        dict(graphs=[
            dict(
                dict(
                    label=p.label
                ),
                **graph_schema.dump(_get_graph_from_project(p))
            ) for p in project_graphs
        ]
        )
    )


__all__ = (
    "adapter_multi_project_graph_as_json",
    "adapter_single_project_graph_as_json"
)
