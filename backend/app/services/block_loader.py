"""Chargement de la bibliothèque de blocs Lego depuis les fichiers JSON statiques."""

import json
from pathlib import Path
from app.config import settings
from app.schemas.block import Block


# Cache en mémoire pour éviter de relire les fichiers à chaque requête
_blocks_cache: list[Block] | None = None


def load_blocks(force_reload: bool = False) -> list[Block]:
    """Charge tous les blocs depuis le dossier blocks/.

    Args:
        force_reload: si True, ignore le cache et relit les fichiers.
    """
    global _blocks_cache
    if _blocks_cache is not None and not force_reload:
        return _blocks_cache

    blocks: list[Block] = []
    base = Path(settings.blocks_dir)
    if not base.exists():
        _blocks_cache = []
        return _blocks_cache

    for json_file in sorted(base.rglob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            block = Block(**data)
            blocks.append(block)
        except Exception as e:
            print(f"[WARN] Échec du chargement de {json_file}: {e}")

    _blocks_cache = blocks
    return blocks


def get_block_by_id(block_id: str) -> Block | None:
    """Retrouve un bloc par son identifiant."""
    return next((b for b in load_blocks() if b.id == block_id), None)
