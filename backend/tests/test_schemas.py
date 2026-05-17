"""Tests de validation des schémas Pydantic."""

import pytest
from pydantic import ValidationError

from app.schemas.block import Block, BlockNode, BlockEdge, BlockLevel
from app.schemas.graph import GraphNode, GraphEdge, FullGraph, GraphUpdate
from app.schemas.diagnosis import Diagnosis, NodeMetrics


def test_block_minimal():
    block = Block(
        id="b1",
        name="Test",
        level=BlockLevel.MACRO,
        school="Test",
        nodes=[BlockNode(id="n1", label="N1")],
        edges=[],
    )
    assert block.id == "b1"
    assert block.level == BlockLevel.MACRO


def test_block_level_invalid():
    with pytest.raises(ValidationError):
        Block(
            id="b1", name="Test", level="invalide", school="Test",
            nodes=[], edges=[],
        )


def test_graph_node_defaults():
    n = GraphNode(id="x", label="X", level=BlockLevel.MESO)
    assert n.capacity == 1.0
    assert n.performance == 1.0
    assert n.workload == 0.5


def test_full_graph_empty():
    g = FullGraph()
    assert g.macro_nodes == []
    assert g.memberships_macro_meso == []


def test_graph_update_default_focus():
    payload = GraphUpdate(graph=FullGraph())
    assert payload.focus_level == BlockLevel.MACRO
    assert payload.focus_node_id is None


def test_node_metrics_default_not_bottleneck():
    m = NodeMetrics(node_id="x")
    assert m.is_bottleneck is False
    assert m.betweenness == 0.0
