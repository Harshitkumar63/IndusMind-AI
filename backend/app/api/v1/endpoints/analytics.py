"""
IndusMind AI — Analytics Endpoints

Dashboard summaries, trend data, and visualization data.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_summary(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get dashboard summary cards and recent activity."""
    return {
        "total_documents": 1247,
        "total_equipment": 342,
        "total_incidents": 89,
        "compliance_score": 81.6,
        "maintenance_due": 12,
        "active_users": 28,
        "knowledge_nodes": 2840,
        "ai_queries_today": 156,
        "recent_uploads": [
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "title": "Centrifugal Pump P-101 Maintenance Manual",
                "original_filename": "P-101_Manual.pdf",
                "file_type": "pdf",
                "file_size": 4523000,
                "category": "manual",
                "status": "ready",
                "processing_progress": 100.0,
                "chunk_count": 47,
                "uploaded_at": "2025-06-15T09:30:00Z",
            },
            {
                "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
                "title": "Safety SOP — Hot Work Permit",
                "original_filename": "SOP_Hot_Work.pdf",
                "file_type": "pdf",
                "file_size": 1892000,
                "category": "sop",
                "status": "ready",
                "processing_progress": 100.0,
                "chunk_count": 23,
                "uploaded_at": "2025-06-14T14:20:00Z",
            },
            {
                "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
                "title": "Boiler Inspection Report 2025",
                "original_filename": "Boiler_Inspection.pdf",
                "file_type": "pdf",
                "file_size": 8734000,
                "category": "inspection",
                "status": "ready",
                "processing_progress": 100.0,
                "chunk_count": 62,
                "uploaded_at": "2025-06-10T11:00:00Z",
            },
        ],
    }


@router.get("/incidents")
async def get_incident_trends(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get incident trends by month."""
    return [
        {"month": "Jan 2025", "critical": 1, "major": 3, "minor": 8, "observation": 12},
        {"month": "Feb 2025", "critical": 0, "major": 2, "minor": 6, "observation": 15},
        {"month": "Mar 2025", "critical": 1, "major": 4, "minor": 9, "observation": 11},
        {"month": "Apr 2025", "critical": 0, "major": 1, "minor": 5, "observation": 14},
        {"month": "May 2025", "critical": 2, "major": 3, "minor": 7, "observation": 10},
        {"month": "Jun 2025", "critical": 0, "major": 2, "minor": 4, "observation": 13},
    ]


@router.get("/equipment-health")
async def get_equipment_health_rankings(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get equipment health rankings."""
    return [
        {
            "equipment_id": "P-101",
            "name": "Centrifugal Pump P-101",
            "health_score": 78.5,
            "incident_count": 3,
            "maintenance_count": 12,
            "status": "running",
        },
        {
            "equipment_id": "B-401",
            "name": "Water Tube Boiler B-401",
            "health_score": 65.0,
            "incident_count": 5,
            "maintenance_count": 18,
            "status": "running",
        },
        {
            "equipment_id": "C-201",
            "name": "Reciprocating Compressor C-201",
            "health_score": 71.2,
            "incident_count": 2,
            "maintenance_count": 8,
            "status": "running",
        },
        {
            "equipment_id": "E-301",
            "name": "Heat Exchanger E-301",
            "health_score": 82.0,
            "incident_count": 2,
            "maintenance_count": 6,
            "status": "maintenance",
        },
        {
            "equipment_id": "T-801",
            "name": "Steam Turbine T-801",
            "health_score": 88.5,
            "incident_count": 1,
            "maintenance_count": 15,
            "status": "running",
        },
        {
            "equipment_id": "V-501",
            "name": "Pressure Vessel V-501",
            "health_score": 92.0,
            "incident_count": 0,
            "maintenance_count": 4,
            "status": "running",
        },
        {
            "equipment_id": "M-601",
            "name": "Induction Motor M-601",
            "health_score": 95.0,
            "incident_count": 0,
            "maintenance_count": 3,
            "status": "running",
        },
        {
            "equipment_id": "TV-701",
            "name": "Control Valve TV-701",
            "health_score": 85.0,
            "incident_count": 1,
            "maintenance_count": 5,
            "status": "running",
        },
    ]


@router.get("/compliance-trend")
async def get_compliance_trend(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get compliance score trend over time."""
    return [
        {"label": "Jan 2025", "value": 76.0},
        {"label": "Feb 2025", "value": 78.5},
        {"label": "Mar 2025", "value": 80.0},
        {"label": "Apr 2025", "value": 79.0},
        {"label": "May 2025", "value": 82.0},
        {"label": "Jun 2025", "value": 81.6},
    ]


@router.get("/maintenance-trend")
async def get_maintenance_trend(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get maintenance activity trend."""
    return [
        {"label": "Jan 2025", "preventive": 12, "corrective": 5, "predictive": 3, "breakdown": 1},
        {"label": "Feb 2025", "preventive": 15, "corrective": 3, "predictive": 4, "breakdown": 0},
        {"label": "Mar 2025", "preventive": 10, "corrective": 6, "predictive": 2, "breakdown": 2},
        {"label": "Apr 2025", "preventive": 14, "corrective": 4, "predictive": 5, "breakdown": 1},
        {"label": "May 2025", "preventive": 11, "corrective": 7, "predictive": 3, "breakdown": 1},
        {"label": "Jun 2025", "preventive": 13, "corrective": 4, "predictive": 6, "breakdown": 2},
    ]


@router.get("/document-growth")
async def get_document_growth(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get document ingestion growth over time."""
    return [
        {"label": "Jan 2025", "value": 892},
        {"label": "Feb 2025", "value": 945},
        {"label": "Mar 2025", "value": 1023},
        {"label": "Apr 2025", "value": 1089},
        {"label": "May 2025", "value": 1178},
        {"label": "Jun 2025", "value": 1247},
    ]


@router.get("/document-categories")
async def get_document_categories(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get document distribution by category."""
    return [
        {"name": "Manuals", "value": 312, "color": "#6366f1"},
        {"name": "SOPs", "value": 245, "color": "#8b5cf6"},
        {"name": "Inspection Reports", "value": 198, "color": "#a78bfa"},
        {"name": "Maintenance Logs", "value": 178, "color": "#c4b5fd"},
        {"name": "Regulations", "value": 142, "color": "#818cf8"},
        {"name": "Audit Reports", "value": 98, "color": "#7c3aed"},
        {"name": "Others", "value": 74, "color": "#4f46e5"},
    ]
