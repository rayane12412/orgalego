"""Tests unitaires des algorithmes de théorie des graphes."""

import networkx as nx
import pytest

from app.core.algorithms.communities import detect_communities
from app.core.algorithms.centrality import compute_betweenness, compute_pagerank
from app.core.algorithms.archetypes import euclidean_distance, match_archetypes
from app.schemas.block import Block, BlockLevel


# ----------- Centralité d'intermédiarité -----------

def test_betweenness_empty_graph():
    g = nx.Graph()
    assert compute_betweenness(g) == []


def test_betweenness_star_graph():
    """Sur un graphe en étoile, le centre a la betweenness maximale."""
    g = nx.star_graph(5)  # nœud 0 au centre, 1..5 en feuilles
    metrics = compute_betweenness(g)
    # Le centre (0) doit être en tête
    assert metrics[0].node_id == "0"
    assert metrics[0].betweenness > 0
    # Les feuilles ont une betweenness nulle
    for m in metrics[1:]:
        assert m.betweenness == 0.0


def test_betweenness_detects_bottleneck():
    """Sur un graphe en étoile à 6 nœuds, le centre dépasse le seuil de 0.3."""
    g = nx.star_graph(5)
    metrics = compute_betweenness(g, bottleneck_threshold=0.3)
    bottlenecks = [m for m in metrics if m.is_bottleneck]
    assert len(bottlenecks) == 1
    assert bottlenecks[0].node_id == "0"


# ----------- Louvain -----------

def test_louvain_empty_graph():
    g = nx.Graph()
    result = detect_communities(g)
    assert result.modularity == 0.0
    assert result.n_communities == 0


def test_louvain_two_cliques():
    """Deux cliques reliées par une seule arête doivent former 2 communautés."""
    g = nx.Graph()
    # Clique A : 0-1-2
    g.add_edges_from([(0, 1), (1, 2), (0, 2)])
    # Clique B : 3-4-5
    g.add_edges_from([(3, 4), (4, 5), (3, 5)])
    # Pont
    g.add_edge(2, 3)
    result = detect_communities(g)
    assert result.n_communities >= 2
    assert result.modularity > 0.3


# ----------- PageRank -----------

def test_pagerank_empty_graph():
    g = nx.Graph()
    assert compute_pagerank(g) == {}


def test_pagerank_returns_scores():
    g = nx.star_graph(5)
    pr = compute_pagerank(g)
    assert len(pr) == 6
    assert all(0.0 <= v <= 1.0 for v in pr.values())


# ----------- Archétypes -----------

def test_euclidean_distance_zero():
    obs = {"depth": 2.0, "span": 5.0, "density": 0.4}
    dist, gaps = euclidean_distance(obs, obs)
    assert dist == pytest.approx(0.0)
    assert all(g == 0.0 for g in gaps.values())


def test_euclidean_distance_positive():
    obs = {"depth": 3.0, "span": 4.0}
    target = {"depth": 2.0, "span": 5.0}
    dist, _ = euclidean_distance(obs, target)
    assert dist > 0.0


def test_match_archetypes_returns_sorted():
    obs = {"depth": 2.0, "span": 5.0, "density": 0.33}
    arch_a = Block(
        id="a", name="A", level=BlockLevel.MACRO, school="Test",
        nodes=[], edges=[], signature={"depth": 2.0, "span": 5.0, "density": 0.33},
    )
    arch_b = Block(
        id="b", name="B", level=BlockLevel.MACRO, school="Test",
        nodes=[], edges=[], signature={"depth": 10.0, "span": 1.0, "density": 0.9},
    )
    matches = match_archetypes(obs, [arch_b, arch_a])
    # A doit être le meilleur match (distance nulle)
    assert matches[0].archetype_name == "A"
    assert matches[0].similarity > matches[1].similarity
