"""Schémas Pydantic des résultats de diagnostic."""

from pydantic import BaseModel, Field


class NodeMetrics(BaseModel):
    """Métriques calculées pour un nœud."""
    node_id: str
    betweenness: float = 0.0
    degree: int = 0
    is_bottleneck: bool = False  # True si betweenness > seuil


class CommunityResult(BaseModel):
    """Résultat de la détection de communautés (Louvain)."""
    modularity: float
    communities: dict[str, int] = Field(
        ..., description="node_id -> community_id"
    )
    n_communities: int
    is_siloed: bool = Field(
        default=False,
        description="True si la partition algorithmique reflète des silos",
    )


class ArchetypeMatch(BaseModel):
    """Distance à un archétype théorique."""
    archetype_name: str
    school: str
    distance: float
    similarity: float = Field(..., description="1 / (1 + distance), entre 0 et 1")
    dimensional_gaps: dict[str, float] = Field(
        default_factory=dict,
        description="Écart par dimension (depth, span, density, ...)",
    )


class Recommendation(BaseModel):
    """Recommandation textuelle générée par le diagnostic."""
    severity: str = "info"  # info, warning, critical
    message: str
    related_nodes: list[str] = []


class Diagnosis(BaseModel):
    """Résultat complet d'un diagnostic."""
    node_metrics: list[NodeMetrics]
    community_result: CommunityResult | None = None
    best_archetype: ArchetypeMatch | None = None
    all_archetypes: list[ArchetypeMatch] = []
    recommendations: list[Recommendation] = []
    computed_at: str = ""  # ISO timestamp
