"""Conversion du graphe JSON envoyé par le frontend en objets NetworkX."""

import networkx as nx
from app.schemas.graph import FullGraph, GraphNode, GraphEdge


def build_subgraph(nodes: list[GraphNode], edges: list[GraphEdge]) -> nx.Graph:
    """Construit un graphe NetworkX non orienté à partir d'une liste de nœuds et arêtes."""
    g = nx.Graph()
    for node in nodes:
        g.add_node(
            node.id,
            label=node.label,
            type=node.type,
            level=node.level.value,
            capacity=node.capacity,
            cost=node.cost,
            performance=node.performance,
            workload=node.workload,
        )
    for edge in edges:
        # Si l'arête mentionne des nœuds inexistants, on l'ignore silencieusement
        if edge.source in g.nodes and edge.target in g.nodes:
            g.add_edge(
                edge.source,
                edge.target,
                id=edge.id,
                type=edge.type,
                weight=edge.weight,
                frequency=edge.frequency,
            )
    return g


def build_directed_subgraph(nodes: list[GraphNode], edges: list[GraphEdge]) -> nx.DiGraph:
    """Variante orientée (utile pour la hiérarchie stricte)."""
    g = nx.DiGraph()
    for node in nodes:
        g.add_node(node.id, **node.model_dump())
    for edge in edges:
        if edge.source in g.nodes and edge.target in g.nodes:
            g.add_edge(edge.source, edge.target, **edge.model_dump())
    return g


def build_macro(graph: FullGraph) -> nx.Graph:
    """Construit le graphe macro."""
    return build_subgraph(graph.macro_nodes, graph.macro_edges)


def build_meso(graph: FullGraph, parent_macro_id: str | None = None) -> nx.Graph:
    """Construit le graphe méso, éventuellement restreint à un parent macro."""
    if parent_macro_id is None:
        return build_subgraph(graph.meso_nodes, graph.meso_edges)
    # Filtrer les nœuds méso rattachés au parent macro
    rattachements = {m.child for m in graph.memberships_macro_meso if m.parent == parent_macro_id}
    nodes = [n for n in graph.meso_nodes if n.id in rattachements]
    edges = [e for e in graph.meso_edges if e.source in rattachements and e.target in rattachements]
    return build_subgraph(nodes, edges)


def build_micro(graph: FullGraph, parent_meso_id: str | None = None) -> nx.Graph:
    """Construit le graphe micro, éventuellement restreint à un parent méso."""
    if parent_meso_id is None:
        return build_subgraph(graph.micro_nodes, graph.micro_edges)
    rattachements = {m.child for m in graph.memberships_meso_micro if m.parent == parent_meso_id}
    nodes = [n for n in graph.micro_nodes if n.id in rattachements]
    edges = [e for e in graph.micro_edges if e.source in rattachements and e.target in rattachements]
    return build_subgraph(nodes, edges)
