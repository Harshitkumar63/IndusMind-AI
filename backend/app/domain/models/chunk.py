"""
IndusMind AI — Chunk Model

Stores text chunks created from documents, with references to vector embeddings.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.domain.models.document import Document


class Chunk(Base):
    __tablename__ = "chunks"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    embedding_id: Mapped[str | None] = mapped_column(String(255), default=None)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Relationships
    document: Mapped[Document] = relationship("Document", back_populates="chunks")

    def __repr__(self) -> str:
        return f"<Chunk {self.document_id}:{self.chunk_index}>"
