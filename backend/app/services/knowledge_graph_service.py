"""
IndusMind AI — Knowledge Graph Service

Manages knowledge graph construction, querying, and visualization.
"""

from __future__ import annotations

from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger
from app.infrastructure.graph_db import graph_db

settings = get_settings()
logger = get_logger(__name__)

# ─── Demo knowledge graph ───────────────────────────────────

DEMO_GRAPH = {
    "nodes": [
        {"id": "n1", "node_type": "equipment", "name": "Pump P-101", "properties": {"type": "centrifugal", "manufacturer": "Sulzer", "year": 2019}},
        {"id": "n2", "node_type": "equipment", "name": "Compressor C-201", "properties": {"type": "reciprocating", "manufacturer": "Atlas Copco"}},
        {"id": "n3", "node_type": "equipment", "name": "Heat Exchanger E-301", "properties": {"type": "shell_and_tube"}},
        {"id": "n4", "node_type": "equipment", "name": "Boiler B-401", "properties": {"type": "fire_tube", "capacity": "20 TPH"}},
        {"id": "n5", "node_type": "department", "name": "Mechanical Engineering"},
        {"id": "n6", "node_type": "department", "name": "Process Engineering"},
        {"id": "n7", "node_type": "department", "name": "Safety Department"},
        {"id": "n8", "node_type": "person", "name": "Rajesh Kumar", "properties": {"role": "Sr. Maintenance Engineer", "department": "Mechanical"}},
        {"id": "n9", "node_type": "person", "name": "Priya Sharma", "properties": {"role": "Safety Officer", "department": "Safety"}},
        {"id": "n10", "node_type": "person", "name": "Amit Patel", "properties": {"role": "Plant Manager"}},
        {"id": "n11", "node_type": "location", "name": "Unit-1 Process Area"},
        {"id": "n12", "node_type": "location", "name": "Unit-2 Utilities"},
        {"id": "n13", "node_type": "sop", "name": "SOP-M-001", "properties": {"title": "Pump Maintenance Procedure"}},
        {"id": "n14", "node_type": "sop", "name": "SOP-S-003", "properties": {"title": "Hot Work Permit Procedure"}},
        {"id": "n15", "node_type": "regulation", "name": "OSHA PSM 1910.119", "properties": {"section": "Process Safety Management"}},
        {"id": "n16", "node_type": "regulation", "name": "ISO 10816-3", "properties": {"section": "Vibration Severity"}},
        {"id": "n17", "node_type": "incident", "name": "INC-042: Mechanical Seal Leak", "properties": {"date": "2025-03-15", "severity": "minor"}},
        {"id": "n18", "node_type": "incident", "name": "INC-038: Tube Failure", "properties": {"date": "2025-01-22", "severity": "major"}},
        {"id": "n19", "node_type": "process", "name": "Cooling Water System"},
        {"id": "n20", "node_type": "material", "name": "316 Stainless Steel"},
    ],
    "edges": [
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
    ],
}


class KnowledgeGraphService:
    """Manages knowledge graph operations."""

    async def get_full_graph(self) -> dict[str, Any]:
        """Retrieve the complete knowledge graph for visualization."""
        if settings.DEMO_MODE:
            return DEMO_GRAPH
        return await graph_db.get_full_graph()

    async def add_entities_from_document(
        self,
        entities: dict[str, list[dict[str, Any]]],
        relationships: list[dict[str, Any]],
    ) -> dict[str, int]:
        """Add entities and relationships from a processed document to the graph."""
        if settings.DEMO_MODE:
            total_entities = sum(len(v) for v in entities.values())
            return {"nodes_created": total_entities, "edges_created": len(relationships)}

        node_ids: dict[str, str] = {}
        nodes_created = 0

        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                neo4j_id = await graph_db.create_node(
                    node_type=entity_type.capitalize(),
                    name=entity["name"],
                    properties=entity.get("properties", {}),
                )
                if neo4j_id:
                    node_ids[entity["name"]] = neo4j_id
                    nodes_created += 1

        edges_created = 0
        for rel in relationships:
            source_id = node_ids.get(rel["source"])
            target_id = node_ids.get(rel["target"])
            if source_id and target_id:
                await graph_db.create_relationship(
                    source_id=source_id,
                    target_id=target_id,
                    relationship=rel["relationship"].upper(),
                )
                edges_created += 1

        return {"nodes_created": nodes_created, "edges_created": edges_created}

    async def search_nodes(self, query: str, node_type: str | None = None) -> list[dict]:
        """Search nodes in the knowledge graph."""
        if settings.DEMO_MODE:
            q_lower = query.lower()
            return [
                node for node in DEMO_GRAPH["nodes"]
                if q_lower in node["name"].lower()
                and (node_type is None or node["node_type"] == node_type)
            ]
        return await graph_db.search_nodes(query, node_type)

    async def get_stats(self) -> dict[str, Any]:
        """Get knowledge graph statistics."""
        if settings.DEMO_MODE:
            type_counts: dict[str, int] = {}
            for node in DEMO_GRAPH["nodes"]:
                type_counts[node["node_type"]] = type_counts.get(node["node_type"], 0) + 1
            return {
                "total_nodes": len(DEMO_GRAPH["nodes"]),
                "total_edges": len(DEMO_GRAPH["edges"]),
                "node_types": type_counts,
            }
        graph = await graph_db.get_full_graph()
        return {
            "total_nodes": len(graph["nodes"]),
            "total_edges": len(graph["edges"]),
        }


# Singleton
knowledge_graph_service = KnowledgeGraphService()
