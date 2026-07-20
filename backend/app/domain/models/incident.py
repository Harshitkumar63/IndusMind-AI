"""
IndusMind AI — Incident Model

Stores industrial incidents linked to equipment.
"""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import IncidentSeverity, IncidentStatus
from app.infrastructure.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    equipment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("equipment.id", ondelete="SET NULL"),
        index=True, default=None,
    )
    reported_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"),
        default=None,
    )
    incident_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    severity: Mapped[IncidentSeverity] = mapped_column(
        String(50), default=IncidentSeverity.MINOR
    )
    status: Mapped[IncidentStatus] = mapped_column(
        String(50), default=IncidentStatus.OPEN, index=True
    )
    root_cause: Mapped[str | None] = mapped_column(Text, default=None)
    corrective_action: Mapped[str | None] = mapped_column(Text, default=None)
    incident_date: Mapped[date | None] = mapped_column(Date, default=None)
    resolved_date: Mapped[date | None] = mapped_column(Date, default=None)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Relationships
    equipment: Mapped["Equipment | None"] = relationship(
        "Equipment", back_populates="incidents"
    )

    def __repr__(self) -> str:
        return f"<Incident {self.incident_number}: {self.title}>"


from app.domain.models.equipment import Equipment  # noqa: E402
