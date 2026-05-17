"""Schémas Pydantic du graphe hiérarchique à 3 niveaux."""

from pydantic import BaseModel, Field
from app.schemas.block import BlockLevel


class GraphNode(BaseModel):
    """Un nœud du graphe organisationnel."""
    id: str
    label: str
    level: BlockLevel
    type: str = "default"
    capacity: float = 1.0
    cost: float = 0.0
    performance: float = 1.0
    workload: float = 0.5  # entre 0 et 1
    x: float = 0.0  # position pour rendu 2D
    y: float = 0.0


class GraphEdge(BaseModel):
    """Une arête intra-niveau."""
    id: str
    source: str
    target: str
    type: str = "hierarchy"
    weight: float = 1.0
    frequency: float = 1.0  # fréquence d'interaction


class MembershipEdge(BaseModel):
    """Une arête inter-niveau (rattachement)."""
    id: str
    child: str   # nœud du niveau inférieur
    parent: str  # nœud du niveau supérieur
    weight: float = 1.0  # % de temps alloué (1.0 = 100%)
    is_primary: bool = True


class FullGraph(BaseModel):
    """Le graphe complet à 3 niveaux."""
    macro_nodes: list[GraphNode] = []
    macro_edges: list[GraphEdge] = []
    meso_nodes: list[GraphNode] = []
    meso_edges: list[GraphEdge] = []
    micro_nodes: list[GraphNode] = []
    micro_edges: list[GraphEdge] = []
    memberships_macro_meso: list[MembershipEdge] = []
    memberships_meso_micro: list[MembershipEdge] = []


class GraphUpdate(BaseModel):
    """Message envoyé par le frontend pour signaler une modification."""
    graph: FullGraph
    focus_level: BlockLevel = BlockLevel.MACRO
    focus_node_id: str | None = Field(
        default=None,
        description="Nœud parent dont on regarde le sous-graphe (None = vue macro globale)",
    )
