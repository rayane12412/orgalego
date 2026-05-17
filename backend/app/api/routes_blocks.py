"""Route GET /blocks : catalogue de la bibliothèque Lego."""

from fastapi import APIRouter, HTTPException
from app.schemas.block import Block, BlockLevel
from app.services.block_loader import load_blocks, get_block_by_id

router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.get("", response_model=list[Block])
def list_blocks(level: BlockLevel | None = None) -> list[Block]:
    """Liste tous les blocs disponibles, filtrable par niveau."""
    blocks = load_blocks()
    if level is not None:
        blocks = [b for b in blocks if b.level == level]
    return blocks


@router.get("/{block_id}", response_model=Block)
def get_block(block_id: str) -> Block:
    """Récupère un bloc par identifiant."""
    block = get_block_by_id(block_id)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Bloc inconnu : {block_id}")
    return block
