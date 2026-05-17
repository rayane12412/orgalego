"""Outils de gestion de la hiérarchie à 3 niveaux."""

import networkx as nx
from app.schemas.graph import FullGraph
from app.schemas.block import BlockLevel
from app.core.graph_builder import build_macro, build_meso, build_micro


def get_graph_at_level(
    graph: FullGraph,
    level: BlockLevel,
    focus_node_id: str | None = None,
) -> nx.Graph:
    """Retourne le sous-graphe correspondant au niveau demandé.

    Si focus_node_id est fourni, on ne retourne que le sous-graphe rattaché à ce parent.
    """
    if level == BlockLevel.MACRO:
        return build_macro(graph)
    if level == BlockLevel.MESO:
        return build_meso(graph, parent_macro_id=focus_node_id)
    if level == BlockLevel.MICRO:
        return build_micro(graph, parent_meso_id=focus_node_id)
    raise ValueError(f"Niveau inconnu : {level}")


def compute_structural_signature(g: nx.Graph) -> dict[str, float]:
    """Calcule la signature structurelle d'un graphe (utilisée pour le matching d'archétypes)."""
    if g.number_of_nodes() == 0:
        return {"depth": 0.0, "span": 0.0, "density": 0.0, "modularity": 0.0, "supervisor_ratio": 0.0}

    # Profondeur : plus long plus court chemin (diamètre) sur composante connexe
    try:
        if nx.is_connected(g):
            depth = float(nx.diameter(g))
        else:
            # Diamètre sur la plus grande composante
            largest_cc = max(nx.connected_components(g), key=len)
            depth = float(nx.diameter(g.subgraph(largest_cc)))
    except Exception:
        depth = 0.0

    # Span moyen : degré moyen
    degrees = [d for _, d in g.degree()]
    span = float(sum(degrees) / len(degrees)) if degrees else 0.0

    # Densité
    density = float(nx.density(g))

    # Ratio de superviseurs (nœuds de type 'manager' ou 'division')
    supervisor_types = {"manager", "division"}
    supervisors = [n for n, attr in g.nodes(data=True) if attr.get("type") in supervisor_types]
    supervisor_ratio = float(len(supervisors) / g.number_of_nodes()) if g.number_of_nodes() else 0.0

    return {
        "depth": depth,
        "span": span,
        "density": density,
        "modularity": 0.0,  # rempli après détection de communautés
        "supervisor_ratio": supervisor_ratio,
    }
