"""
IndusMind AI — Database Seed Script

Populates the database with realistic industrial demo data for hackathon presentation.
Run: python -m app.seed
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


def generate_seed_data() -> dict[str, list[dict[str, Any]]]:
    """Generate comprehensive seed data for all modules."""

    now = datetime.now(timezone.utc)

    # ─── Equipment ─────────────────────────────────────
    equipment = [
        {"id": str(uuid.uuid4()), "tag": "P-101", "name": "Centrifugal Pump P-101", "equipment_type": "pump", "manufacturer": "Sulzer", "model": "MSD-D 100/4", "location": "Unit-1 Process Area", "status": "running", "health_score": 78.5, "install_date": "2019-03-15"},
        {"id": str(uuid.uuid4()), "tag": "C-201", "name": "Reciprocating Compressor C-201", "equipment_type": "compressor", "manufacturer": "Atlas Copco", "model": "GA 90+", "location": "Unit-1 Process Area", "status": "running", "health_score": 71.2, "install_date": "2018-07-22"},
        {"id": str(uuid.uuid4()), "tag": "E-301", "name": "Shell & Tube Heat Exchanger E-301", "equipment_type": "heat_exchanger", "manufacturer": "TEMA", "model": "BEM 600", "location": "Unit-2 Utilities", "status": "running", "health_score": 82.0, "install_date": "2017-11-10"},
        {"id": str(uuid.uuid4()), "tag": "B-401", "name": "Fire Tube Boiler B-401", "equipment_type": "boiler", "manufacturer": "Thermax", "model": "FT 20 TPH", "location": "Unit-2 Utilities", "status": "running", "health_score": 65.0, "install_date": "2016-02-28"},
        {"id": str(uuid.uuid4()), "tag": "T-801", "name": "Cooling Tower T-801", "equipment_type": "cooling_tower", "manufacturer": "Hamon", "model": "CT-250", "location": "Unit-2 Utilities", "status": "running", "health_score": 88.5, "install_date": "2020-01-15"},
        {"id": str(uuid.uuid4()), "tag": "V-501", "name": "Pressure Vessel V-501", "equipment_type": "vessel", "manufacturer": "L&T", "model": "PV-1000", "location": "Unit-1 Process Area", "status": "running", "health_score": 92.0, "install_date": "2019-08-20"},
        {"id": str(uuid.uuid4()), "tag": "M-601", "name": "Electric Motor M-601", "equipment_type": "motor", "manufacturer": "ABB", "model": "M3BP 315", "location": "Unit-1 Process Area", "status": "running", "health_score": 95.0, "install_date": "2021-04-12"},
        {"id": str(uuid.uuid4()), "tag": "TV-701", "name": "Temperature Control Valve TV-701", "equipment_type": "valve", "manufacturer": "Fisher", "model": "GX", "location": "Unit-1 Process Area", "status": "running", "health_score": 85.0, "install_date": "2020-09-05"},
    ]

    # ─── Documents ─────────────────────────────────────
    documents = [
        {"id": str(uuid.uuid4()), "title": "Centrifugal Pump P-101 Maintenance Manual", "filename": "P-101_Manual.pdf", "file_type": "pdf", "file_size": 4523000, "category": "manual", "status": "ready", "page_count": 124, "chunk_count": 47, "uploaded_at": (now - timedelta(days=2)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Safety SOP — Hot Work Permit Procedure", "filename": "SOP_Hot_Work.pdf", "file_type": "pdf", "file_size": 1892000, "category": "sop", "status": "ready", "page_count": 32, "chunk_count": 23, "uploaded_at": (now - timedelta(days=3)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Annual Boiler Inspection Report 2025", "filename": "Boiler_Inspection.pdf", "file_type": "pdf", "file_size": 8734000, "category": "inspection", "status": "ready", "page_count": 78, "chunk_count": 62, "uploaded_at": (now - timedelta(days=7)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "OSHA Process Safety Management Guidelines", "filename": "OSHA_PSM.pdf", "file_type": "pdf", "file_size": 12456000, "category": "regulation", "status": "ready", "page_count": 156, "chunk_count": 89, "uploaded_at": (now - timedelta(days=9)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Vibration Analysis Report — Compressor C-201", "filename": "Vibration_C201.xlsx", "file_type": "xlsx", "file_size": 2134000, "category": "report", "status": "ready", "page_count": 4, "chunk_count": 18, "uploaded_at": (now - timedelta(days=5)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Heat Exchanger E-301 Failure Investigation", "filename": "HX_E301_Report.pdf", "file_type": "pdf", "file_size": 5678000, "category": "report", "status": "ready", "page_count": 45, "chunk_count": 34, "uploaded_at": (now - timedelta(days=6)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "ISO 45001 OHS Management System Manual", "filename": "ISO_45001_Manual.pdf", "file_type": "pdf", "file_size": 6789000, "category": "regulation", "status": "ready", "page_count": 89, "chunk_count": 56, "uploaded_at": (now - timedelta(days=1)).isoformat()},
        {"id": str(uuid.uuid4()), "title": "Quarterly Maintenance Log — Q2 2025", "filename": "Maintenance_Q2_2025.xlsx", "file_type": "xlsx", "file_size": 3456000, "category": "maintenance", "status": "ready", "page_count": 12, "chunk_count": 28, "uploaded_at": (now - timedelta(days=4)).isoformat()},
    ]

    # ─── Incidents ─────────────────────────────────────
    incidents = [
        {"id": str(uuid.uuid4()), "incident_number": "INC-2025-042", "title": "Mechanical Seal Leak on Pump P-101", "severity": "minor", "status": "closed", "equipment_tag": "P-101", "reported_at": (now - timedelta(days=90)).isoformat(), "description": "Minor seal leak detected during routine patrol. No environmental release."},
        {"id": str(uuid.uuid4()), "incident_number": "INC-2025-038", "title": "Tube Failure in Heat Exchanger E-301", "severity": "major", "status": "investigating", "equipment_tag": "E-301", "reported_at": (now - timedelta(days=145)).isoformat(), "description": "Tube-side leak detected via pressure drop. Root cause: 316 SS stress corrosion cracking."},
        {"id": str(uuid.uuid4()), "incident_number": "INC-2025-051", "title": "Safety Valve Lifting Below Set Pressure", "severity": "critical", "status": "open", "equipment_tag": "B-401", "reported_at": (now - timedelta(days=15)).isoformat(), "description": "SV-401A lifting at 8.2 bar (set: 10.5 bar). Boiler derated pending investigation."},
    ]

    # ─── Maintenance Records ───────────────────────────
    maintenance = [
        {"id": str(uuid.uuid4()), "work_order": "WO-2025-0312", "title": "P-101 Quarterly Vibration Analysis", "maintenance_type": "predictive", "priority": "medium", "status": "completed", "equipment_tag": "P-101", "scheduled_date": (now - timedelta(days=5)).isoformat(), "cost": 1200},
        {"id": str(uuid.uuid4()), "work_order": "WO-2025-0318", "title": "B-401 Safety Valve Inspection", "maintenance_type": "corrective", "priority": "urgent", "status": "in_progress", "equipment_tag": "B-401", "scheduled_date": now.isoformat(), "cost": 8500},
        {"id": str(uuid.uuid4()), "work_order": "WO-2025-0305", "title": "C-201 Valve Plate Replacement", "maintenance_type": "preventive", "priority": "high", "status": "overdue", "equipment_tag": "C-201", "scheduled_date": (now - timedelta(days=5)).isoformat(), "cost": 4200},
        {"id": str(uuid.uuid4()), "work_order": "WO-2025-0320", "title": "T-801 Annual Basin Cleaning", "maintenance_type": "preventive", "priority": "low", "status": "scheduled", "equipment_tag": "T-801", "scheduled_date": (now + timedelta(days=15)).isoformat(), "cost": 3500},
    ]

    # ─── Compliance ────────────────────────────────────
    compliance = [
        {"id": str(uuid.uuid4()), "regulation": "API 510", "standard_name": "Pressure Vessel Inspection Code", "score": 95, "status": "compliant", "last_audit": (now - timedelta(days=30)).isoformat(), "next_audit": (now + timedelta(days=335)).isoformat()},
        {"id": str(uuid.uuid4()), "regulation": "ISO 45001", "standard_name": "Occupational Health & Safety", "score": 88, "status": "compliant", "last_audit": (now - timedelta(days=60)).isoformat(), "next_audit": (now + timedelta(days=305)).isoformat()},
        {"id": str(uuid.uuid4()), "regulation": "OSHA PSM", "standard_name": "Process Safety Management", "score": 85, "status": "compliant", "last_audit": (now - timedelta(days=45)).isoformat(), "next_audit": (now + timedelta(days=320)).isoformat()},
        {"id": str(uuid.uuid4()), "regulation": "ISO 14001", "standard_name": "Environmental Management System", "score": 55, "status": "non_compliant", "last_audit": (now - timedelta(days=20)).isoformat(), "next_audit": (now + timedelta(days=70)).isoformat()},
    ]

    return {
        "equipment": equipment,
        "documents": documents,
        "incidents": incidents,
        "maintenance": maintenance,
        "compliance": compliance,
    }


def main() -> None:
    """Print seed data summary (database insertion requires running DB)."""
    setup_logging()
    data = generate_seed_data()
    logger.info("Seed data generated:")
    for key, records in data.items():
        logger.info(f"  {key}: {len(records)} records")
    print("\n✅ Seed data ready. Connect to PostgreSQL to insert.")


if __name__ == "__main__":
    main()
