"""
IndusMind AI — User Model

Stores platform users synced from Clerk authentication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import UserRole
from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.domain.models.conversation import Conversation
    from app.domain.models.document import Document


class User(Base):
    __tablename__ = "users"

    clerk_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(String(50), default=UserRole.VIEWER)
    department: Mapped[str | None] = mapped_column(String(255), default=None)
    avatar_url: Mapped[str | None] = mapped_column(Text, default=None)
    preferences: Mapped[dict | None] = mapped_column(JSONB, default=None)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    documents: Mapped[list[Document]] = relationship("Document", back_populates="user", lazy="selectin")
    conversations: Mapped[list[Conversation]] = relationship("Conversation", back_populates="user", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"
