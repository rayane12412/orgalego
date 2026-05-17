"""Schémas Pydantic des blocs Lego (templates organisationnels)."""

from enum import Enum
from pydantic import BaseModel, Field


class BlockLevel(str, Enum):
    """Niveau hiérarchique d'un bloc."""
    MACRO = "macro"
    MESO = "meso"
    MICRO = "micro"


class BlockNode(BaseModel):
    """Un nœud d'un bloc Lego."""
    id: str
    label: str
    type: str = "default"  # division, equipe, manager, expert, etc.
    capacity: float = 1.0
    cost: float = 0.0


class BlockEdge(BaseModel):
    """Une arête entre deux nœuds d'un bloc."""
    source: str
    target: str
    type: str = "hierarchy"  # hierarchy, functional, collaboration, informal
    weight: float = 1.0


class Block(BaseModel):
    """Un bloc Lego complet : template d'archétype organisationnel."""
    id: str
    name: str = Field(..., description="Nom lisible du bloc")
    level: BlockLevel
    school: str = Field(..., description="École théorique : Mintzberg, Fayol, etc.")
    description: str = ""
    nodes: list[BlockNode]
    edges: list[BlockEdge]

    # Signature structurelle utilisée par le matching d'archétypes
    signature: dict[str, float] = Field(
        default_factory=dict,
        description="Métriques attendues : depth, span, density, modularity, etc.",
    )
