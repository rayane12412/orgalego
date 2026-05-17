"""Orchestrateur principal : appelle les 3 algorithmes du MVP et agrège les résultats."""

from datetime import datetime, timezone
import networkx as nx

from app.schemas.graph import FullGraph
from app.schemas.block import Block, BlockLevel
from app.schemas.diagnosis import Diagnosis, Recommendation
from app.core.multilevel import get_graph_at_level, compute_structural_signature
from app.core.algorithms.communities import detect_communities
from app.core.algorithms.centrality import compute_betweenness
from app.core.algorithms.archetypes import match_archetypes


def run_full_diagnosis(
    graph: FullGraph,
    archetypes: list[Block],
    focus_level: BlockLevel = BlockLevel.MACRO,
    focus_node_id: str | None = None,
) -> Diagnosis:
    """Lance les 3 algorithmes du MVP sur le sous-graphe en focus.

    Args:
        graph: graphe complet à 3 niveaux.
        archetypes: liste des blocs Lego servant de référence théorique.
        focus_level: niveau analysé (macro / méso / micro).
        focus_node_id: si fourni, restreint au sous-graphe rattaché à ce parent.
    """
    g: nx.Graph = get_graph_at_level(graph, focus_level, focus_node_id)

    # 1) Centralité d'intermédiarité
    node_metrics = compute_betweenness(g, weight="frequency")

    # 2) Détection de communautés (Louvain)
    community_result = detect_communities(g, weight="frequency")

    # 3) Matching d'archétypes (sur le bon niveau)
    relevant_archetypes = [a for a in archetypes if a.level == focus_level]
    observed_signature = compute_structural_signature(g)
    observed_signature["modularity"] = community_result.modularity
    matches = match_archetypes(observed_signature, relevant_archetypes)

    # Recommandations dérivées
    recommendations = _build_recommendations(node_metrics, community_result, matches)

    return Diagnosis(
        node_metrics=node_metrics,
        community_result=community_result,
        best_archetype=matches[0] if matches else None,
        all_archetypes=matches,
        recommendations=recommendations,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


def _build_recommendations(node_metrics, community_result, archetype_matches) -> list[Recommendation]:
    """Génère des recommandations textuelles à partir des résultats algorithmiques."""
    recos: list[Recommendation] = []

    # Goulots
    bottlenecks = [m for m in node_metrics if m.is_bottleneck]
    if bottlenecks:
        recos.append(
            Recommendation(
                severity="warning",
                message=(
                    f"{len(bottlenecks)} nœud(s) identifié(s) comme goulot(s) d'étranglement. "
                    "Envisager un rôle de liaison secondaire ou un by-pass."
                ),
                related_nodes=[m.node_id for m in bottlenecks],
            )
        )

    # Silos
    if community_result and community_result.is_siloed:
        recos.append(
            Recommendation(
                severity="warning",
                message=(
                    f"Organisation silotée détectée (modularité = {community_result.modularity}, "
                    f"{community_result.n_communities} communautés)."
                ),
            )
        )

    # Archétype dominant
    if archetype_matches:
        best = archetype_matches[0]
        if best.similarity >= 0.6:
            recos.append(
                Recommendation(
                    severity="info",
                    message=(
                        f"Configuration la plus proche : {best.archetype_name} "
                        f"(école {best.school}, similarité {best.similarity})."
                    ),
                )
            )
        else:
            recos.append(
                Recommendation(
                    severity="warning",
                    message=(
                        f"Aucun archétype théorique ne matche fortement (meilleur : "
                        f"{best.archetype_name}, similarité {best.similarity}). "
                        "Possible incohérence structurelle."
                    ),
                )
            )

    return recos
