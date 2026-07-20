"""
IndusMind AI — Compliance Record Model

Stores compliance audit records against regulatory standards.
"""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ComplianceStandard, ComplianceStatus
from app.infrastructure.database import Base


class ComplianceRecord(Base):
    __tablename__ = "compliance_records"

    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"),
        index=True, default=None,
    )
    auditor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"),
        default=None,
    )
    regulation_ref: Mapped[str | None] = mapped_column(String(500), default=None)
    standard: Mapped[ComplianceStandard] = mapped_column(String(50))
    category: Mapped[str | None] = mapped_column(String(255), default=None)
    status: Mapped[ComplianceStatus] = mapped_column(
        String(50), default=ComplianceStatus.PENDING, index=True
    )
    score: Mapped[float | None] = mapped_column(Float, default=None)
    findings: Mapped[list[str] | None] = mapped_column(ARRAY(Text), default=None)
    violations: Mapped[list[str] | None] = mapped_column(ARRAY(Text), default=None)
    recommendations: Mapped[list[str] | None] = mapped_column(ARRAY(Text), default=None)
    audit_date: Mapped[date | None] = mapped_column(Date, default=None)
    next_audit_date: Mapped[date | None] = mapped_column(Date, default=None)

    def __repr__(self) -> str:
        return f"<ComplianceRecord {self.standard}: {self.status}>"
