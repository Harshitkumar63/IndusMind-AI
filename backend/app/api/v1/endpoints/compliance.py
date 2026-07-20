"""
IndusMind AI — Compliance Endpoints

Compliance auditing, scoring, and violation tracking.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user

router = APIRouter()

DEMO_COMPLIANCE = [
    {"id": "c-001", "regulation_ref": "OSHA 29 CFR 1910.119(e)", "standard": "osha", "category": "Process Hazard Analysis", "status": "compliant", "score": 92.0, "findings": ["PHA review completed on schedule", "All action items closed"], "violations": [], "recommendations": ["Update PHA for recent process changes"], "audit_date": "2025-05-15", "next_audit_date": "2026-05-15", "created_at": "2025-05-15T00:00:00Z"},
    {"id": "c-002", "regulation_ref": "OSHA 29 CFR 1910.119(j)", "standard": "osha", "category": "Mechanical Integrity", "status": "partially", "score": 78.0, "findings": ["3 of 5 equipment inspections completed", "Piping inspection schedule behind"], "violations": ["Overdue inspection for high-pressure piping in Unit-1"], "recommendations": ["Accelerate piping inspection schedule", "Add contractor support for NDE testing"], "audit_date": "2025-05-20", "next_audit_date": "2025-11-20", "created_at": "2025-05-20T00:00:00Z"},
    {"id": "c-003", "regulation_ref": "ISO 45001:2018 Section 6.1", "standard": "iso_45001", "category": "Actions to Address Risks", "status": "compliant", "score": 88.0, "findings": ["Risk register updated quarterly", "Emergency drills conducted as planned"], "violations": [], "recommendations": ["Expand near-miss reporting program"], "audit_date": "2025-04-10", "next_audit_date": "2025-10-10", "created_at": "2025-04-10T00:00:00Z"},
    {"id": "c-004", "regulation_ref": "ISO 14001:2015 Section 8.1", "standard": "iso_14001", "category": "Operational Planning and Control", "status": "non_compliant", "score": 55.0, "findings": ["Environmental monitoring gaps identified", "Waste disposal records incomplete"], "violations": ["Missing air emission monitoring data for Q1 2025", "Hazardous waste storage exceeding 90-day limit"], "recommendations": ["Install continuous emission monitors", "Implement digital waste tracking system", "Schedule immediate hazardous waste pickup"], "audit_date": "2025-06-01", "next_audit_date": "2025-09-01", "created_at": "2025-06-01T00:00:00Z"},
    {"id": "c-005", "regulation_ref": "API 510 Section 7", "standard": "api", "category": "Pressure Vessel Inspection", "status": "compliant", "score": 95.0, "findings": ["All vessels inspected within schedule", "Corrosion rates within acceptable limits"], "violations": [], "recommendations": ["Consider upgrading V-501 relief valve"], "audit_date": "2025-03-25", "next_audit_date": "2025-09-25", "created_at": "2025-03-25T00:00:00Z"},
]


@router.get("")
async def list_compliance(
    standard: str | None = None,
    status: str | None = None,
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """List compliance records."""
    items = DEMO_COMPLIANCE
    if standard:
        items = [c for c in items if c["standard"] == standard]
    if status:
        items = [c for c in items if c["status"] == status]
    return items


@router.get("/score")
async def get_compliance_score(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get overall compliance score breakdown."""
    return {
        "overall_score": 81.6,
        "by_standard": {
            "osha": 85.0,
            "iso_45001": 88.0,
            "iso_14001": 55.0,
            "api": 95.0,
        },
        "total_audits": 24,
        "compliant_count": 18,
        "non_compliant_count": 2,
        "pending_count": 4,
        "active_violations": 3,
    }


@router.get("/violations")
async def get_violations(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get active compliance violations."""
    return [
        {"id": "v-001", "regulation": "OSHA 29 CFR 1910.119(j)", "description": "Overdue inspection for high-pressure piping in Unit-1", "severity": "major", "status": "open", "days_open": 25, "assigned_to": "Rajesh Kumar"},
        {"id": "v-002", "regulation": "ISO 14001:2015 Section 8.1", "description": "Missing air emission monitoring data for Q1 2025", "severity": "major", "status": "in_progress", "days_open": 14, "assigned_to": "Priya Sharma"},
        {"id": "v-003", "regulation": "ISO 14001:2015 Section 8.1", "description": "Hazardous waste storage exceeding 90-day limit", "severity": "critical", "status": "open", "days_open": 5, "assigned_to": "Amit Patel"},
    ]


@router.get("/audit-summary")
async def get_audit_summary(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get AI-generated audit summary."""
    return {
        "summary": "The plant's overall compliance posture is MODERATE (81.6%). While API and ISO 45001 standards show strong compliance, ISO 14001 environmental compliance is a critical gap requiring immediate attention. OSHA Mechanical Integrity program has minor deficiencies that should be addressed within the next audit cycle.",
        "key_findings": [
            "Environmental management system has significant gaps in monitoring and waste disposal",
            "Process safety management is largely compliant with minor improvement areas",
            "Pressure vessel inspection program is exemplary — can serve as model for other programs",
            "Occupational health and safety risk management is well-established",
        ],
        "critical_violations": [
            "Hazardous waste storage exceeding 90-day regulatory limit — immediate action required",
            "Missing continuous emission monitoring data — regulatory reporting at risk",
        ],
        "recommendations": [
            "URGENT: Address hazardous waste storage violation within 48 hours",
            "Install continuous emission monitoring systems in Q3 2025",
            "Accelerate mechanical integrity piping inspection program",
            "Implement digital compliance tracking platform to replace manual spreadsheets",
            "Schedule cross-functional compliance review meeting within 2 weeks",
        ],
        "risk_areas": [
            "Environmental compliance (ISO 14001) — HIGH RISK",
            "Mechanical integrity inspections — MEDIUM RISK",
            "Contractor safety management — LOW RISK",
        ],
    }


@router.post("/analyze")
async def analyze_compliance(
    document_id: str | None = None,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Run compliance analysis on a document."""
    return {
        "status": "completed",
        "document_id": document_id,
        "compliance_score": 82.0,
        "standards_checked": ["osha", "iso_45001", "api"],
        "gaps_found": 3,
        "recommendations": 5,
    }
