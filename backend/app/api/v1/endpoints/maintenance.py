"""
IndusMind AI — Maintenance Endpoints

Maintenance records, intelligence, and predictions.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user
from app.schemas import MaintenanceCreate, MaintenanceResponse, StatusResponse

router = APIRouter()

DEMO_MAINTENANCE = [
    {"id": "m-001", "work_order": "WO-2025-0142", "type": "preventive", "priority": "medium", "status": "completed", "description": "Quarterly vibration analysis and bearing inspection for P-101", "scheduled_date": "2025-03-15", "completed_date": "2025-03-15", "cost": 2500.0, "downtime_hours": 4.0, "created_at": "2025-03-01T00:00:00Z"},
    {"id": "m-002", "work_order": "WO-2025-0156", "type": "corrective", "priority": "high", "status": "completed", "description": "Mechanical seal replacement on P-101 due to leak detected", "scheduled_date": "2025-04-02", "completed_date": "2025-04-03", "cost": 8500.0, "downtime_hours": 12.0, "created_at": "2025-04-01T00:00:00Z"},
    {"id": "m-003", "work_order": "WO-2025-0178", "type": "preventive", "priority": "medium", "status": "scheduled", "description": "Annual tube bundle inspection for E-301", "scheduled_date": "2025-07-01", "completed_date": None, "cost": None, "downtime_hours": None, "created_at": "2025-06-01T00:00:00Z"},
    {"id": "m-004", "work_order": "WO-2025-0189", "type": "predictive", "priority": "high", "status": "overdue", "description": "Compressor C-201 valve plate inspection — vibration trending high", "scheduled_date": "2025-06-10", "completed_date": None, "cost": None, "downtime_hours": None, "created_at": "2025-05-20T00:00:00Z"},
    {"id": "m-005", "work_order": "WO-2025-0195", "type": "breakdown", "priority": "urgent", "status": "in_progress", "description": "Emergency repair — Boiler B-401 safety valve stuck open", "scheduled_date": "2025-06-14", "completed_date": None, "cost": 15000.0, "downtime_hours": 8.0, "created_at": "2025-06-14T00:00:00Z"},
    {"id": "m-006", "work_order": "WO-2025-0201", "type": "preventive", "priority": "low", "status": "scheduled", "description": "Motor M-601 annual insulation resistance test", "scheduled_date": "2025-07-15", "completed_date": None, "cost": None, "downtime_hours": None, "created_at": "2025-06-10T00:00:00Z"},
]


@router.get("", response_model=list[MaintenanceResponse])
async def list_maintenance(
    status: str | None = None,
    type: str | None = None,
    priority: str | None = None,
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """List maintenance records with optional filters."""
    items = DEMO_MAINTENANCE
    if status:
        items = [m for m in items if m["status"] == status]
    if type:
        items = [m for m in items if m["type"] == type]
    if priority:
        items = [m for m in items if m["priority"] == priority]
    return items


@router.post("", response_model=StatusResponse)
async def create_maintenance(
    data: MaintenanceCreate,
    user: dict[str, Any] = Depends(get_current_user),
) -> StatusResponse:
    """Create a new maintenance record."""
    return StatusResponse(status="ok", message=f"Maintenance record {data.work_order} created")


@router.get("/intelligence")
async def get_maintenance_intelligence(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get AI-generated maintenance intelligence insights."""
    return {
        "total_records": 156,
        "overdue_count": 3,
        "avg_downtime_hours": 6.2,
        "total_cost": 245000.0,
        "critical_equipment": [
            {"equipment_id": "P-101", "name": "Centrifugal Pump P-101", "health_score": 78.5, "risk_level": "medium", "days_since_maintenance": 92, "predicted_failure_days": 145, "recommendations": ["Schedule vibration check", "Monitor bearing temperature"]},
            {"equipment_id": "B-401", "name": "Water Tube Boiler B-401", "health_score": 65.0, "risk_level": "high", "days_since_maintenance": 108, "predicted_failure_days": 90, "recommendations": ["Urgent safety valve inspection", "Review water treatment program"]},
            {"equipment_id": "C-201", "name": "Reciprocating Compressor C-201", "health_score": 71.2, "risk_level": "medium", "days_since_maintenance": 66, "predicted_failure_days": 120, "recommendations": ["Valve plate inspection overdue", "Check piston rod packing"]},
        ],
        "failure_predictions": [
            {"equipment": "P-101", "component": "Mechanical Seal", "probability": 0.35, "timeline": "60-90 days", "impact": "Process shutdown"},
            {"equipment": "B-401", "component": "Safety Valve", "probability": 0.55, "timeline": "30-45 days", "impact": "Critical safety risk"},
            {"equipment": "C-201", "component": "Valve Plate", "probability": 0.42, "timeline": "45-75 days", "impact": "Reduced capacity"},
        ],
        "recommendations": [
            "Prioritize Boiler B-401 safety valve inspection — highest failure probability",
            "Schedule P-101 seal replacement during next planned shutdown",
            "Implement condition-based monitoring for C-201 valve plates",
            "Review spare parts inventory for critical equipment",
            "Consider upgrading to API 682 seal plan for P-101",
        ],
    }


@router.get("/predictions")
async def get_failure_predictions(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get simulated failure predictions for equipment."""
    return [
        {"equipment_id": "P-101", "equipment_name": "Centrifugal Pump P-101", "component": "Mechanical Seal", "failure_probability": 0.35, "remaining_useful_life_days": 145, "risk_level": "medium", "recommendation": "Plan replacement at next turnaround"},
        {"equipment_id": "B-401", "equipment_name": "Water Tube Boiler B-401", "component": "Safety Valve SV-401A", "failure_probability": 0.55, "remaining_useful_life_days": 90, "risk_level": "high", "recommendation": "Immediate inspection required"},
        {"equipment_id": "C-201", "equipment_name": "Reciprocating Compressor C-201", "component": "Suction Valve Plate", "failure_probability": 0.42, "remaining_useful_life_days": 120, "risk_level": "medium", "recommendation": "Schedule inspection within 2 weeks"},
        {"equipment_id": "E-301", "equipment_name": "Heat Exchanger E-301", "component": "Tube Bundle", "failure_probability": 0.28, "remaining_useful_life_days": 200, "risk_level": "low", "recommendation": "Monitor shell-side pressure drop trend"},
    ]


@router.get("/overdue")
async def get_overdue_maintenance(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get overdue maintenance items."""
    return [m for m in DEMO_MAINTENANCE if m["status"] == "overdue"]
