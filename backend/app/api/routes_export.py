"""Endpoint d'export du diagnostic en PDF ou JSON."""

from fastapi import APIRouter
from fastapi.responses import Response
from app.schemas.graph import GraphUpdate
from app.services.block_loader import load_blocks
from app.services.export_service import export_diagnosis_to_pdf, export_diagnosis_to_json
from app.core.diagnosis import run_full_diagnosis

router = APIRouter(prefix="/export", tags=["export"])


@router.post("/pdf")
def export_pdf(payload: GraphUpdate) -> Response:
    """Génère un rapport PDF du diagnostic."""
    diagnosis = run_full_diagnosis(
        payload.graph, load_blocks(), payload.focus_level, payload.focus_node_id
    )
    pdf_bytes = export_diagnosis_to_pdf(diagnosis)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=orgalego_diagnosis.pdf"},
    )


@router.post("/json")
def export_json(payload: GraphUpdate) -> Response:
    """Export brut du diagnostic en JSON."""
    diagnosis = run_full_diagnosis(
        payload.graph, load_blocks(), payload.focus_level, payload.focus_node_id
    )
    return Response(
        content=export_diagnosis_to_json(diagnosis),
        media_type="application/json",
    )
