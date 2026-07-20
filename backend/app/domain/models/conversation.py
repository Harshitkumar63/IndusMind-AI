"""
IndusMind AI — Conversation & Message Models

Stores AI chat conversations with message history, citations, and confidence scores.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import MessageRole
from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.domain.models.user import User


class Conversation(Base):
    __tablename__ = "conversations"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(500), default="New Conversation")
    context_type: Mapped[str | None] = mapped_column(String(100), default=None)
    context_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), default=None
    )
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan",
        order_by="Message.created_at", lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Conversation {self.title}>"


class Message(Base):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[MessageRole] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    citations: Mapped[dict | None] = mapped_column(JSONB, default=None)
    confidence_score: Mapped[float | None] = mapped_column(Float, default=None)
    suggested_questions: Mapped[list[str] | None] = mapped_column(
        ARRAY(String(500)), default=None
    )
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )

    def __repr__(self) -> str:
        return f"<Message {self.role}: {self.content[:50]}>"
