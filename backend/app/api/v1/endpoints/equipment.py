"""
IndusMind AI — Equipment Endpoints

Equipment CRUD and health assessment.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user
from app.schemas import (
    EquipmentCreate,
    EquipmentHealthResponse,
    EquipmentResponse,
    StatusResponse,
)

router = APIRouter()

DEMO_EQUIPMENT = [
    {
        "id": "eq-001",
        "equipment_id": "P-101",
        "name": "Centrifugal Pump P-101",
        "type": "pump",
        "department": "Mechanical",
        "location": "Unit-1 Process Area",
        "criticality": "critical",
        "status": "running",
        "install_date": "2018-03-15",
        "last_maintenance": "2025-03-15",
        "next_maintenance": "2025-06-15",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-002",
        "equipment_id": "C-201",
        "name": "Reciprocating Compressor C-201",
        "type": "compressor",
        "department": "Mechanical",
        "location": "Unit-1 Process Area",
        "criticality": "critical",
        "status": "running",
        "install_date": "2019-07-20",
        "last_maintenance": "2025-04-10",
        "next_maintenance": "2025-07-10",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-003",
        "equipment_id": "E-301",
        "name": "Shell & Tube Heat Exchanger E-301",
        "type": "heat_exchanger",
        "department": "Process",
        "location": "Unit-2 Utilities",
        "criticality": "high",
        "status": "maintenance",
        "install_date": "2017-11-05",
        "last_maintenance": "2025-05-20",
        "next_maintenance": "2025-08-20",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-004",
        "equipment_id": "B-401",
        "name": "Water Tube Boiler B-401",
        "type": "boiler",
        "department": "Utilities",
        "location": "Unit-2 Utilities",
        "criticality": "critical",
        "status": "running",
        "install_date": "2016-01-10",
        "last_maintenance": "2025-02-28",
        "next_maintenance": "2025-05-28",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-005",
        "equipment_id": "V-501",
        "name": "Pressure Vessel V-501",
        "type": "vessel",
        "department": "Process",
        "location": "Unit-1 Process Area",
        "criticality": "high",
        "status": "running",
        "install_date": "2020-05-12",
        "last_maintenance": "2025-05-01",
        "next_maintenance": "2025-11-01",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-006",
        "equipment_id": "M-601",
        "name": "Induction Motor M-601",
        "type": "motor",
        "department": "Electrical",
        "location": "Unit-1 Process Area",
        "criticality": "medium",
        "status": "running",
        "install_date": "2021-09-30",
        "last_maintenance": "2025-04-15",
        "next_maintenance": "2025-10-15",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-007",
        "equipment_id": "TV-701",
        "name": "Control Valve TV-701",
        "type": "valve",
        "department": "Instrumentation",
        "location": "Unit-1 Process Area",
        "criticality": "medium",
        "status": "running",
        "install_date": "2019-02-14",
        "last_maintenance": "2025-01-20",
        "next_maintenance": "2025-07-20",
        "created_at": "2025-01-01T00:00:00Z",
    },
    {
        "id": "eq-008",
        "equipment_id": "T-801",
        "name": "Steam Turbine T-801",
        "type": "turbine",
        "department": "Power",
        "location": "Unit-3 Power House",
        "criticality": "critical",
        "status": "running",
        "install_date": "2015-06-22",
        "last_maintenance": "2025-06-01",
        "next_maintenance": "2025-09-01",
        "created_at": "2025-01-01T00:00:00Z",
    },
]


@router.get("", response_model=list[EquipmentResponse])
async def list_equipment(
    type: str | None = None,
    status: str | None = None,
    criticality: str | None = None,
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """List all equipment with optional filters."""
    items = DEMO_EQUIPMENT
    if type:
        items = [e for e in items if e["type"] == type]
    if status:
        items = [e for e in items if e["status"] == status]
    if criticality:
        items = [e for e in items if e["criticality"] == criticality]
    return items


@router.get("/{equipment_id}")
async def get_equipment(
    equipment_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get equipment details with incident/maintenance history."""
    eq = next(
        (e for e in DEMO_EQUIPMENT if e["equipment_id"] == equipment_id or e["id"] == equipment_id), DEMO_EQUIPMENT[0]
    )
    return {
        **eq,
        "specifications": {"flow_rate": "150 m³/h", "pressure": "12 bar", "material": "316SS"},
        "description": "Critical process pump for unit-1 feed system",
        "incident_count": 3,
        "maintenance_count": 12,
    }


@router.post("", response_model=StatusResponse)
async def create_equipment(
    data: EquipmentCreate,
    user: dict[str, Any] = Depends(get_current_user),
) -> StatusResponse:
    """Create a new equipment record."""
    return StatusResponse(status="ok", message=f"Equipment {data.equipment_id} created")


@router.get("/{equipment_id}/health", response_model=EquipmentHealthResponse)
async def get_equipment_health(
    equipment_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get AI-generated health assessment for equipment."""
    return {
        "equipment_id": equipment_id,
        "name": "Centrifugal Pump P-101",
        "health_score": 78.5,
        "risk_level": "medium",
        "days_since_maintenance": 92,
        "predicted_failure_days": 145,
        "recommendations": [
            "Schedule vibration analysis within next 2 weeks",
            "Monitor bearing temperature — trending upward",
            "Replace mechanical seal at next planned shutdown",
            "Review lubrication schedule per manufacturer specs",
        ],
    }
