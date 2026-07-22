"""
IndusMind AI — Document Model

Stores uploaded document metadata, processing status, and extracted text.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import DocumentCategory, DocumentStatus, DocumentType
from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.domain.models.chunk import Chunk
    from app.domain.models.user import User


class Document(Base):
    __tablename__ = "documents"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(500))
    original_filename: Mapped[str] = mapped_column(String(500))
    file_path: Mapped[str] = mapped_column(Text)
    file_type: Mapped[DocumentType] = mapped_column(String(50))
    file_size: Mapped[int] = mapped_column(BigInteger)
    category: Mapped[DocumentCategory] = mapped_column(String(50), default=DocumentCategory.OTHER)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(100)), default=None)
    status: Mapped[DocumentStatus] = mapped_column(String(50), default=DocumentStatus.UPLOADING, index=True)
    processing_progress: Mapped[float] = mapped_column(Float, default=0.0)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, default=None)
    extracted_text: Mapped[str | None] = mapped_column(Text, default=None)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    processed_at: Mapped[datetime | None] = mapped_column(default=None)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="documents")
    chunks: Mapped[list[Chunk]] = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Document {self.title} ({self.status})>"
