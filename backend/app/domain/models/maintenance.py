"""
IndusMind AI — Maintenance Record Model

Stores maintenance work orders and history for equipment.
"""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import MaintenancePriority, MaintenanceStatus, MaintenanceType
from app.infrastructure.database import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    equipment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("equipment.id", ondelete="SET NULL"),
        index=True, default=None,
    )
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"),
        default=None,
    )
    work_order: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    type: Mapped[MaintenanceType] = mapped_column(String(50))
    priority: Mapped[MaintenancePriority] = mapped_column(
        String(50), default=MaintenancePriority.MEDIUM
    )
    status: Mapped[MaintenanceStatus] = mapped_column(
        String(50), default=MaintenanceStatus.SCHEDULED, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, default=None)
    findings: Mapped[str | None] = mapped_column(Text, default=None)
    actions_taken: Mapped[str | None] = mapped_column(Text, default=None)
    scheduled_date: Mapped[date | None] = mapped_column(Date, default=None)
    completed_date: Mapped[date | None] = mapped_column(Date, default=None)
    cost: Mapped[float | None] = mapped_column(Float, default=None)
    downtime_hours: Mapped[float | None] = mapped_column(Float, default=None)
    parts_used: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Relationships
    equipment: Mapped["Equipment | None"] = relationship(
        "Equipment", back_populates="maintenance_records"
    )

    def __repr__(self) -> str:
        return f"<MaintenanceRecord {self.work_order}: {self.status}>"


from app.domain.models.equipment import Equipment  # noqa: E402
