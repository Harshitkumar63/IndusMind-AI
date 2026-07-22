"""
IndusMind AI — Equipment Model

Stores industrial equipment records with health tracking.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import EquipmentCriticality, EquipmentStatus, EquipmentType
from app.infrastructure.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment="Plant tag e.g. P-101")
    name: Mapped[str] = mapped_column(String(500))
    type: Mapped[EquipmentType] = mapped_column(String(50))
    department: Mapped[str | None] = mapped_column(String(255), default=None)
    location: Mapped[str | None] = mapped_column(String(500), default=None)
    criticality: Mapped[EquipmentCriticality] = mapped_column(String(50), default=EquipmentCriticality.MEDIUM)
    status: Mapped[EquipmentStatus] = mapped_column(String(50), default=EquipmentStatus.RUNNING, index=True)
    install_date: Mapped[date | None] = mapped_column(Date, default=None)
    last_maintenance: Mapped[date | None] = mapped_column(Date, default=None)
    next_maintenance: Mapped[date | None] = mapped_column(Date, default=None)
    specifications: Mapped[dict | None] = mapped_column(JSONB, default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationships
    incidents: Mapped[list[Incident]] = relationship("Incident", back_populates="equipment", lazy="selectin")
    maintenance_records: Mapped[list[MaintenanceRecord]] = relationship(
        "MaintenanceRecord", back_populates="equipment", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Equipment {self.equipment_id}: {self.name}>"


# Avoid circular import at module level
from app.domain.models.incident import Incident  # noqa: E402
from app.domain.models.maintenance import MaintenanceRecord  # noqa: E402
