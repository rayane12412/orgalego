"""Centralité d'intermédiarité (betweenness) - détection des goulots d'étranglement.

Inclut aussi le PageRank, reporté en v2 mais déjà implémenté pour faciliter l'extension future.
"""

import networkx as nx
from app.schemas.diagnosis import NodeMetrics


def compute_betweenness(
    g: nx.Graph,
    weight: str | None = None,
    bottleneck_threshold: float = 0.3,
) -> list[NodeMetrics]:
    """Calcule la centralité d'intermédiarité de chaque nœud.

    Args:
        g: graphe à analyser.
        weight: attribut d'arête utilisé (ou None pour graphe non pondéré).
        bottleneck_threshold: seuil au-dessus duquel un nœud est considéré comme goulot.

    Returns:
        Liste de NodeMetrics triée par betweenness décroissante.
    """
    if g.number_of_nodes() == 0:
        return []

    try:
        bc = nx.betweenness_centrality(g, weight=weight, normalized=True)
    except Exception:
        bc = {n: 0.0 for n in g.nodes()}

    results: list[NodeMetrics] = []
    for node_id in g.nodes():
        score = round(float(bc.get(node_id, 0.0)), 4)
        results.append(
            NodeMetrics(
                node_id=str(node_id),
                betweenness=score,
                degree=int(g.degree(node_id)),
                is_bottleneck=score > bottleneck_threshold,
            )
        )

    return sorted(results, key=lambda x: -x.betweenness)


def compute_pagerank(g: nx.Graph, weight: str | None = None) -> dict[str, float]:
    """Calcule le PageRank (v2 : identification des leaders informels).

    Pas encore exposé dans le diagnostic principal mais disponible pour les tests.
    """
    if g.number_of_nodes() == 0:
        return {}

    try:
        pr = nx.pagerank(g, weight=weight)
    except Exception:
        pr = {n: 1.0 / g.number_of_nodes() for n in g.nodes()}

    return {str(node_id): round(float(score), 4) for node_id, score in pr.items()}
