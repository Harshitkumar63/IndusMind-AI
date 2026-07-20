"""
IndusMind AI — Knowledge Graph Endpoints

Knowledge graph visualization data and entity search.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user

router = APIRouter()

# ─── Demo Knowledge Graph ──────────────────────────────────────

DEMO_NODES = [
    {"id": "n1", "node_type": "equipment", "name": "Pump P-101", "properties": {"type": "centrifugal", "criticality": "critical"}},
    {"id": "n2", "node_type": "equipment", "name": "Compressor C-201", "properties": {"type": "reciprocating", "criticality": "critical"}},
    {"id": "n3", "node_type": "equipment", "name": "Heat Exchanger E-301", "properties": {"type": "shell-tube", "criticality": "high"}},
    {"id": "n4", "node_type": "equipment", "name": "Boiler B-401", "properties": {"type": "water-tube", "criticality": "critical"}},
    {"id": "n5", "node_type": "department", "name": "Mechanical Engineering", "properties": {}},
    {"id": "n6", "node_type": "department", "name": "Process Engineering", "properties": {}},
    {"id": "n7", "node_type": "department", "name": "Safety Department", "properties": {}},
    {"id": "n8", "node_type": "person", "name": "Rajesh Kumar", "properties": {"role": "Senior Maintenance Engineer"}},
    {"id": "n9", "node_type": "person", "name": "Priya Sharma", "properties": {"role": "Safety Officer"}},
    {"id": "n10", "node_type": "person", "name": "Amit Patel", "properties": {"role": "Plant Manager"}},
    {"id": "n11", "node_type": "location", "name": "Unit-1 Process Area", "properties": {}},
    {"id": "n12", "node_type": "location", "name": "Unit-2 Utilities", "properties": {}},
    {"id": "n13", "node_type": "sop", "name": "SOP-M-001: Pump Overhaul", "properties": {}},
    {"id": "n14", "node_type": "sop", "name": "SOP-S-003: Hot Work Permit", "properties": {}},
    {"id": "n15", "node_type": "regulation", "name": "OSHA PSM 29 CFR 1910.119", "properties": {}},
    {"id": "n16", "node_type": "regulation", "name": "ISO 10816-3 Vibration", "properties": {}},
    {"id": "n17", "node_type": "incident", "name": "INC-2025-042: Seal Leak P-101", "properties": {"severity": "minor"}},
    {"id": "n18", "node_type": "incident", "name": "INC-2025-038: Tube Failure E-301", "properties": {"severity": "major"}},
    {"id": "n19", "node_type": "process", "name": "Cooling Water System", "properties": {}},
    {"id": "n20", "node_type": "material", "name": "316 Stainless Steel", "properties": {}},
]

DEMO_EDGES = [
    {"source": "n1", "target": "n5", "relationship": "maintained_by"},
    {"source": "n1", "target": "n8", "relationship": "maintained_by"},
    {"source": "n1", "target": "n11", "relationship": "located_in"},
    {"source": "n1", "target": "n13", "relationship": "governed_by"},
    {"source": "n1", "target": "n17", "relationship": "related_to"},
    {"source": "n1", "target": "n16", "relationship": "governed_by"},
    {"source": "n2", "target": "n5", "relationship": "maintained_by"},
    {"source": "n2", "target": "n11", "relationship": "located_in"},
    {"source": "n3", "target": "n6", "relationship": "maintained_by"},
    {"source": "n3", "target": "n12", "relationship": "located_in"},
    {"source": "n3", "target": "n18", "relationship": "related_to"},
    {"source": "n3", "target": "n19", "relationship": "part_of"},
    {"source": "n3", "target": "n20", "relationship": "uses"},
    {"source": "n4", "target": "n12", "relationship": "located_in"},
    {"source": "n4", "target": "n15", "relationship": "governed_by"},
    {"source": "n9", "target": "n7", "relationship": "part_of"},
    {"source": "n10", "target": "n6", "relationship": "part_of"},
    {"source": "n14", "target": "n7", "relationship": "governed_by"},
    {"source": "n17", "target": "n8", "relationship": "inspected_by"},
    {"source": "n18", "target": "n6", "relationship": "inspected_by"},
]


@router.get("")
async def get_knowledge_graph(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get the full knowledge graph (nodes + edges)."""
    return {
        "nodes": DEMO_NODES,
        "edges": DEMO_EDGES,
        "stats": {
            "total_nodes": len(DEMO_NODES),
            "total_edges": len(DEMO_EDGES),
            "node_types": {
                "equipment": 4, "department": 3, "person": 3,
                "location": 2, "sop": 2, "regulation": 2,
                "incident": 2, "process": 1, "material": 1,
            },
        },
    }


@router.get("/nodes")
async def list_nodes(
    node_type: str | None = None,
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """List knowledge graph nodes with optional type filter."""
    nodes = DEMO_NODES
    if node_type:
        nodes = [n for n in nodes if n["node_type"] == node_type]
    return nodes


@router.get("/nodes/{node_id}")
async def get_node(
    node_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get a node with its relationships."""
    node = next((n for n in DEMO_NODES if n["id"] == node_id), DEMO_NODES[0])
    related_edges = [e for e in DEMO_EDGES if e["source"] == node_id or e["target"] == node_id]
    return {**node, "relationships": related_edges}


@router.get("/search")
async def search_graph(
    q: str = Query(..., min_length=1),
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Search knowledge graph by entity name."""
    return [n for n in DEMO_NODES if q.lower() in n["name"].lower()]


@router.get("/stats")
async def get_graph_stats(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get knowledge graph statistics."""
    return {
        "total_nodes": len(DEMO_NODES),
        "total_edges": len(DEMO_EDGES),
        "node_types": {"equipment": 4, "department": 3, "person": 3, "location": 2, "sop": 2, "regulation": 2, "incident": 2, "process": 1, "material": 1},
        "relationship_types": {"maintained_by": 4, "located_in": 4, "governed_by": 4, "related_to": 2, "part_of": 3, "inspected_by": 2, "uses": 1},
    }
