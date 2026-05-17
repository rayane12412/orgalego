"""Détection de communautés par l'algorithme de Louvain (détection de silos)."""

import networkx as nx
from app.schemas.diagnosis import CommunityResult


def detect_communities(g: nx.Graph, weight: str = "frequency") -> CommunityResult:
    """Applique l'algorithme de Louvain et retourne la partition + modularité.

    Args:
        g: graphe à analyser.
        weight: attribut d'arête utilisé comme poids (par défaut 'frequency').

    Returns:
        CommunityResult contenant la partition, la modularité, et le nombre de communautés.
    """
    if g.number_of_nodes() == 0:
        return CommunityResult(modularity=0.0, communities={}, n_communities=0)

    # NetworkX fournit Louvain depuis la version 3.0
    try:
        partition_sets = nx.community.louvain_communities(g, weight=weight, seed=42)
    except Exception:
        # Fallback : chaque nœud dans sa propre communauté
        partition_sets = [{n} for n in g.nodes()]

    # Conversion en dict node_id -> community_id
    communities: dict[str, int] = {}
    for community_id, nodes_set in enumerate(partition_sets):
        for node in nodes_set:
            communities[str(node)] = community_id

    # Modularité
    try:
        modularity = float(nx.community.modularity(g, partition_sets, weight=weight))
    except Exception:
        modularity = 0.0

    n_communities = len(partition_sets)
    # Heuristique simple : une organisation est "silotée" si modularité > 0.4 ET plus d'une communauté
    is_siloed = modularity > 0.4 and n_communities > 1

    return CommunityResult(
        modularity=round(modularity, 4),
        communities=communities,
        n_communities=n_communities,
        is_siloed=is_siloed,
    )
