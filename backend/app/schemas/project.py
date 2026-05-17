"""Schémas Pydantic pour la persistance des projets."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.graph import FullGraph


class ProjectBase(BaseModel):
    """Champs communs aux projets."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""


class ProjectCreate(ProjectBase):
    """Requête de création d'un projet."""
    graph: FullGraph


class ProjectUpdate(BaseModel):
    """Requête de mise à jour d'un projet (champs optionnels)."""
    name: str | None = None
    description: str | None = None
    graph: FullGraph | None = None


class Project(ProjectBase):
    """Projet sauvegardé (renvoi serveur)."""
    id: int
    graph: FullGraph
    created_at: datetime
    updated_at: datetime
