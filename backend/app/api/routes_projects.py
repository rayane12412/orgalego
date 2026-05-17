"""CRUD sur les projets utilisateur."""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ProjectModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.graph import FullGraph

router = APIRouter(prefix="/projects", tags=["projects"])


def _to_schema(model: ProjectModel) -> Project:
    return Project(
        id=model.id,
        name=model.name,
        description=model.description or "",
        graph=FullGraph(**json.loads(model.graph_json)),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


@router.get("", response_model=list[Project])
def list_projects(db: Session = Depends(get_db)) -> list[Project]:
    return [_to_schema(p) for p in db.query(ProjectModel).all()]


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_db)) -> Project:
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    return _to_schema(project)


@router.post("", response_model=Project, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    model = ProjectModel(
        name=payload.name,
        description=payload.description,
        graph_json=payload.graph.model_dump_json(),
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return _to_schema(model)


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)
) -> Project:
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description
    if payload.graph is not None:
        project.graph_json = payload.graph.model_dump_json()
    db.commit()
    db.refresh(project)
    return _to_schema(project)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Projet introuvable")
    db.delete(project)
    db.commit()
