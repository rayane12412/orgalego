"""Tests d'intégration de l'API FastAPI."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_health():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app" in data


def test_list_blocks():
    response = client.get("/blocks")
    assert response.status_code == 200
    blocks = response.json()
    assert isinstance(blocks, list)
    # On a au moins quelques blocs dans la bibliothèque
    assert len(blocks) >= 4


def test_list_blocks_filtered_by_level():
    response = client.get("/blocks?level=macro")
    assert response.status_code == 200
    blocks = response.json()
    assert all(b["level"] == "macro" for b in blocks)


def test_get_block_not_found():
    response = client.get("/blocks/inconnu")
    assert response.status_code == 404


def test_get_known_block():
    response = client.get("/blocks/macro_fonctionnelle")
    assert response.status_code == 200
    assert response.json()["name"] == "Structure fonctionnelle"
