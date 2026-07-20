"""
IndusMind AI — Analytics Service

Aggregates data from all modules into dashboard-ready analytics.
"""

from __future__ import annotations

from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

# ─── Demo Analytics Data ────────────────────────────────────

DEMO_DASHBOARD = {
    "summary": {
        "total_documents": 1247,
        "total_equipment": 342,
        "total_incidents": 89,
        "compliance_score": 81.6,
        "maintenance_due": 12,
        "ai_queries_today": 156,
        "knowledge_nodes": 2840,
        "knowledge_edges": 4210,
    },
    "trends": {
        "documents_change": "+23",
        "equipment_change": "+5",
        "incidents_change": "-12",
        "compliance_change": "+2.1%",
    },
}

DEMO_INCIDENT_TRENDS = [
    {"month": "Jan", "critical": 1, "major": 3, "minor": 8, "observation": 12},
    {"month": "Feb", "critical": 0, "major": 2, "minor": 6, "observation": 15},
    {"month": "Mar", "critical": 1, "major": 4, "minor": 9, "observation": 11},
    {"month": "Apr", "critical": 0, "major": 1, "minor": 5, "observation": 14},
    {"month": "May", "critical": 2, "major": 3, "minor": 7, "observation": 10},
    {"month": "Jun", "critical": 0, "major": 2, "minor": 4, "observation": 13},
]

DEMO_EQUIPMENT_HEALTH = [
    {"name": "P-101", "type": "Centrifugal Pump", "health_score": 78.5, "status": "running", "risk_level": "medium"},
    {"name": "B-401", "type": "Fire Tube Boiler", "health_score": 65.0, "status": "running", "risk_level": "high"},
    {"name": "C-201", "type": "Reciprocating Compressor", "health_score": 71.2, "status": "running", "risk_level": "medium"},
    {"name": "E-301", "type": "Shell & Tube HX", "health_score": 82.0, "status": "running", "risk_level": "low"},
    {"name": "T-801", "type": "Cooling Tower", "health_score": 88.5, "status": "running", "risk_level": "low"},
    {"name": "V-501", "type": "Pressure Vessel", "health_score": 92.0, "status": "running", "risk_level": "low"},
    {"name": "M-601", "type": "Electric Motor", "health_score": 95.0, "status": "running", "risk_level": "low"},
    {"name": "TV-701", "type": "Control Valve", "health_score": 85.0, "status": "running", "risk_level": "low"},
]

DEMO_COMPLIANCE_TREND = [
    {"month": "Jan", "score": 76}, {"month": "Feb", "score": 78.5}, {"month": "Mar", "score": 80},
    {"month": "Apr", "score": 79}, {"month": "May", "score": 82}, {"month": "Jun", "score": 81.6},
]

DEMO_MAINTENANCE_TREND = [
    {"month": "Jan", "preventive": 12, "corrective": 5, "predictive": 3, "breakdown": 1},
    {"month": "Feb", "preventive": 15, "corrective": 3, "predictive": 4, "breakdown": 0},
    {"month": "Mar", "preventive": 10, "corrective": 6, "predictive": 2, "breakdown": 2},
    {"month": "Apr", "preventive": 14, "corrective": 4, "predictive": 5, "breakdown": 1},
    {"month": "May", "preventive": 11, "corrective": 7, "predictive": 3, "breakdown": 1},
    {"month": "Jun", "preventive": 13, "corrective": 4, "predictive": 6, "breakdown": 2},
]

DEMO_DOCUMENT_GROWTH = [
    {"month": "Jan", "total": 892, "new": 45},
    {"month": "Feb", "total": 945, "new": 53},
    {"month": "Mar", "total": 1023, "new": 78},
    {"month": "Apr", "total": 1089, "new": 66},
    {"month": "May", "total": 1178, "new": 89},
    {"month": "Jun", "total": 1247, "new": 69},
]

DEMO_DOCUMENT_CATEGORIES = [
    {"name": "Manuals", "count": 312},
    {"name": "SOPs", "count": 245},
    {"name": "Inspections", "count": 198},
    {"name": "Maintenance Logs", "count": 178},
    {"name": "Regulations", "count": 142},
    {"name": "Audit Reports", "count": 98},
    {"name": "Other", "count": 74},
]


class AnalyticsService:
    """Aggregates analytics across all platform modules."""

    async def get_dashboard(self) -> dict[str, Any]:
        """Get aggregated dashboard data."""
        return DEMO_DASHBOARD

    async def get_incident_trends(self) -> list[dict[str, Any]]:
        """Get incident trends by month and severity."""
        return DEMO_INCIDENT_TRENDS

    async def get_equipment_health(self) -> list[dict[str, Any]]:
        """Get equipment health scores and risk levels."""
        return DEMO_EQUIPMENT_HEALTH

    async def get_compliance_trend(self) -> list[dict[str, Any]]:
        """Get compliance score trend over time."""
        return DEMO_COMPLIANCE_TREND

    async def get_maintenance_trend(self) -> list[dict[str, Any]]:
        """Get maintenance activity trend by type."""
        return DEMO_MAINTENANCE_TREND

    async def get_document_growth(self) -> list[dict[str, Any]]:
        """Get document growth over time."""
        return DEMO_DOCUMENT_GROWTH

    async def get_document_categories(self) -> list[dict[str, Any]]:
        """Get document distribution by category."""
        return DEMO_DOCUMENT_CATEGORIES


# Singleton
analytics_service = AnalyticsService()
