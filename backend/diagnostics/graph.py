from typing import Dict, List
from models.system import SystemDefinition


def build_graph(system: SystemDefinition) -> Dict[str, List[str]]:
    graph = {}

    for component in system.components:
        graph[component.id] = []

    for connection in system.connections:
        if connection.source in graph:
            graph[connection.source].append(connection.target)

    return graph