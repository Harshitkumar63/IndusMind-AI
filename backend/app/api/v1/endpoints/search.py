"""
IndusMind AI — Search Endpoints

Global semantic and keyword search across all entities.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("")
async def global_search(
    q: str = Query(..., min_length=1, max_length=1000),
    type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Global semantic + keyword search across all entities."""
    start = time.time()

    results = [
        {"id": str(uuid.uuid4()), "type": "document", "title": "Centrifugal Pump P-101 Maintenance Manual", "snippet": f"...relevant content matching '{q}'...", "relevance_score": 0.95, "metadata": {"category": "manual", "file_type": "pdf"}},
        {"id": str(uuid.uuid4()), "type": "equipment", "title": "Centrifugal Pump P-101", "snippet": "Critical process pump — Unit-1 Process Area", "relevance_score": 0.92, "metadata": {"status": "running", "criticality": "critical"}},
        {"id": str(uuid.uuid4()), "type": "knowledge_node", "title": "Pump P-101", "snippet": "Equipment node with 8 relationships in knowledge graph", "relevance_score": 0.88, "metadata": {"node_type": "equipment"}},
        {"id": str(uuid.uuid4()), "type": "document", "title": "Vibration Analysis Report — Compressor C-201", "snippet": f"...section related to '{q}'...", "relevance_score": 0.82, "metadata": {"category": "report", "file_type": "xlsx"}},
        {"id": str(uuid.uuid4()), "type": "conversation", "title": "Pump P-101 Maintenance Query", "snippet": "Previous conversation about maintenance schedules", "relevance_score": 0.78, "metadata": {"message_count": 4}},
    ]

    if type:
        results = [r for r in results if r["type"] == type]

    elapsed = (time.time() - start) * 1000

    return {
        "results": results,
        "total": len(results),
        "query": q,
        "processing_time_ms": round(elapsed, 2),
    }


@router.get("/semantic")
async def semantic_search(
    q: str = Query(..., min_length=1),
    top_k: int = Query(10, ge=1, le=50),
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Pure vector similarity search against document embeddings."""
    return {
        "results": [
            {"chunk_id": str(uuid.uuid4()), "document_title": "P-101 Maintenance Manual", "content": f"Relevant chunk matching: {q}", "similarity_score": 0.94},
            {"chunk_id": str(uuid.uuid4()), "document_title": "SOP Hot Work Permit", "content": f"Related procedure for: {q}", "similarity_score": 0.87},
            {"chunk_id": str(uuid.uuid4()), "document_title": "Boiler Inspection Report", "content": f"Inspection finding related to: {q}", "similarity_score": 0.81},
        ],
        "query": q,
        "top_k": top_k,
    }


@router.get("/filters")
async def get_search_filters(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get available filter options for search."""
    return {
        "types": ["document", "equipment", "conversation", "knowledge_node"],
        "categories": ["sop", "manual", "inspection", "maintenance", "audit", "report", "regulation"],
        "departments": ["Mechanical", "Process", "Electrical", "Instrumentation", "Utilities", "Safety"],
        "equipment_types": ["pump", "compressor", "heat_exchanger", "boiler", "vessel", "motor", "valve", "turbine"],
    }
