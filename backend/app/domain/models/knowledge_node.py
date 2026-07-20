"""
IndusMind AI — Knowledge Node & Edge Models

Stores knowledge graph entities and their relationships, mirrored from Neo4j.
"""

from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import KnowledgeNodeType, KnowledgeRelationship
from app.infrastructure.database import Base


class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"

    node_type: Mapped[KnowledgeNodeType] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(500), index=True)
    properties: Mapped[dict | None] = mapped_column(JSONB, default=None)
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"),
        default=None,
    )
    neo4j_id: Mapped[str | None] = mapped_column(String(255), default=None)

    def __repr__(self) -> str:
        return f"<KnowledgeNode {self.node_type}: {self.name}>"


class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"

    source_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("knowledge_nodes.id", ondelete="CASCADE"), index=True
    )
    target_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("knowledge_nodes.id", ondelete="CASCADE"), index=True
    )
    relationship: Mapped[KnowledgeRelationship] = mapped_column(String(50))
    properties: Mapped[dict | None] = mapped_column(JSONB, default=None)
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"),
        default=None,
    )
    confidence: Mapped[float] = mapped_column(Float, default=1.0)

    def __repr__(self) -> str:
        return f"<KnowledgeEdge {self.source_node_id} --{self.relationship}--> {self.target_node_id}>"
