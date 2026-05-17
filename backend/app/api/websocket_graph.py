"""WebSocket pour le diagnostic temps réel."""

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from app.schemas.graph import GraphUpdate
from app.services.block_loader import load_blocks
from app.core.diagnosis import run_full_diagnosis

router = APIRouter()


@router.websocket("/ws/graph")
async def graph_endpoint(ws: WebSocket) -> None:
    """Reçoit les graph_update du frontend et renvoie diagnosis_result."""
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json({"type": "error", "payload": "JSON invalide"})
                continue

            msg_type = msg.get("type")
            if msg_type == "graph_update":
                try:
                    update = GraphUpdate(**msg.get("payload", {}))
                except ValidationError as e:
                    await ws.send_json({"type": "error", "payload": e.errors()})
                    continue

                diagnosis = run_full_diagnosis(
                    graph=update.graph,
                    archetypes=load_blocks(),
                    focus_level=update.focus_level,
                    focus_node_id=update.focus_node_id,
                )
                await ws.send_json(
                    {"type": "diagnosis_result", "payload": diagnosis.model_dump()}
                )
            elif msg_type == "ping":
                await ws.send_json({"type": "pong"})
            else:
                await ws.send_json(
                    {"type": "error", "payload": f"Type de message inconnu : {msg_type}"}
                )
    except WebSocketDisconnect:
        pass
