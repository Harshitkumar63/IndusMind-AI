"""
IndusMind AI — Knowledge Graph Database Infrastructure

Neo4j driver for knowledge graph storage and traversal queries.
"""

from __future__ import annotations

from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class GraphDatabase:
    """Neo4j knowledge graph driver for entity and relationship management."""

    def __init__(self) -> None:
        self._driver: Any = None

    async def connect(self) -> None:
        """Initialize Neo4j connection."""
        if settings.DEMO_MODE:
            logger.info("GraphDB: Running in demo mode")
            return
        try:
            from neo4j import AsyncGraphDatabase as Neo4jDriver

            self._driver = Neo4jDriver.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            )
            async with self._driver.session() as session:
                result = await session.run("RETURN 1 AS test")
                await result.single()
            logger.info("GraphDB: Connected to Neo4j")
        except Exception as e:
            logger.warning("GraphDB: Connection failed", error=str(e))

    async def disconnect(self) -> None:
        """Close Neo4j connection."""
        if self._driver:
            await self._driver.close()

    async def create_node(
        self,
        node_type: str,
        name: str,
        properties: dict[str, Any] | None = None,
    ) -> str | None:
        """Create a node in the knowledge graph. Returns the Neo4j element ID."""
        if not self._driver:
            return None
        props = properties or {}
        props["name"] = name
        prop_str = ", ".join(f"{k}: ${k}" for k in props)
        query = f"CREATE (n:{node_type} {{{prop_str}}}) RETURN elementId(n) AS id"
        async with self._driver.session() as session:
            result = await session.run(query, **props)
            record = await result.single()
            return record["id"] if record else None

    async def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        properties: dict[str, Any] | None = None,
    ) -> None:
        """Create a relationship between two nodes."""
        if not self._driver:
            return
        props = properties or {}
        prop_str = ""
        if props:
            prop_str = " {" + ", ".join(f"{k}: ${k}" for k in props) + "}"
        query = (
            f"MATCH (a) WHERE elementId(a) = $source_id "
            f"MATCH (b) WHERE elementId(b) = $target_id "
            f"CREATE (a)-[r:{relationship}{prop_str}]->(b)"
        )
        async with self._driver.session() as session:
            await session.run(query, source_id=source_id, target_id=target_id, **props)

    async def get_full_graph(self, limit: int = 500) -> dict[str, Any]:
        """Retrieve the full knowledge graph (nodes + relationships)."""
        if not self._driver:
            return {"nodes": [], "edges": []}
        query = f"MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN n, r, m LIMIT {limit}"
        nodes: dict[str, dict] = {}
        edges: list[dict] = []
        async with self._driver.session() as session:
            result = await session.run(query)
            async for record in result:
                n = record["n"]
                node_id = n.element_id
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "node_type": list(n.labels)[0] if n.labels else "unknown",
                        "name": dict(n).get("name", ""),
                        "properties": dict(n),
                    }
                if record["r"] and record["m"]:
                    r = record["r"]
                    m = record["m"]
                    m_id = m.element_id
                    if m_id not in nodes:
                        nodes[m_id] = {
                            "id": m_id,
                            "node_type": list(m.labels)[0] if m.labels else "unknown",
                            "name": dict(m).get("name", ""),
                            "properties": dict(m),
                        }
                    edges.append(
                        {
                            "source": node_id,
                            "target": m_id,
                            "relationship": r.type,
                            "properties": dict(r),
                        }
                    )
        return {"nodes": list(nodes.values()), "edges": edges}

    async def search_nodes(self, name_query: str, node_type: str | None = None) -> list[dict]:
        """Search nodes by name with optional type filter."""
        if not self._driver:
            return []
        if node_type:
            query = f"MATCH (n:{node_type}) WHERE toLower(n.name) CONTAINS toLower($q) RETURN n LIMIT 20"
        else:
            query = "MATCH (n) WHERE toLower(n.name) CONTAINS toLower($q) RETURN n LIMIT 20"
        results: list[dict] = []
        async with self._driver.session() as session:
            result = await session.run(query, q=name_query)
            async for record in result:
                n = record["n"]
                results.append(
                    {
                        "id": n.element_id,
                        "node_type": list(n.labels)[0] if n.labels else "unknown",
                        "name": dict(n).get("name", ""),
                        "properties": dict(n),
                    }
                )
        return results


# Singleton
graph_db = GraphDatabase()
