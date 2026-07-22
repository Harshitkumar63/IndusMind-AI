"""
IndusMind AI — Document Endpoints

Upload, manage, and retrieve industrial documents.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.api.v1.deps import get_current_user
from app.schemas import (
    ChunkResponse,
    DocumentDetailResponse,
    DocumentResponse,
    DocumentUpdate,
    DocumentUploadResponse,
    PaginatedResponse,
    StatusResponse,
)

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".csv", ".txt", ".png", ".jpg", ".jpeg"}

# ─── Demo Data ─────────────────────────────────────────────────

DEMO_DOCUMENTS: list[dict] = [
    {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "title": "Centrifugal Pump P-101 Maintenance Manual",
        "original_filename": "P-101_Maintenance_Manual.pdf",
        "file_type": "pdf",
        "file_size": 4_523_000,
        "category": "manual",
        "tags": ["pump", "centrifugal", "maintenance", "P-101"],
        "status": "ready",
        "processing_progress": 100.0,
        "chunk_count": 47,
        "uploaded_at": "2025-06-15T09:30:00Z",
        "processed_at": "2025-06-15T09:35:00Z",
    },
    {
        "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
        "title": "Safety SOP — Hot Work Permit Procedure",
        "original_filename": "SOP_Hot_Work_Permit.pdf",
        "file_type": "pdf",
        "file_size": 1_892_000,
        "category": "sop",
        "tags": ["safety", "hot-work", "permit", "procedure"],
        "status": "ready",
        "processing_progress": 100.0,
        "chunk_count": 23,
        "uploaded_at": "2025-06-14T14:20:00Z",
        "processed_at": "2025-06-14T14:23:00Z",
    },
    {
        "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "title": "Annual Boiler Inspection Report 2025",
        "original_filename": "Boiler_Inspection_2025.pdf",
        "file_type": "pdf",
        "file_size": 8_734_000,
        "category": "inspection",
        "tags": ["boiler", "inspection", "annual", "2025"],
        "status": "ready",
        "processing_progress": 100.0,
        "chunk_count": 62,
        "uploaded_at": "2025-06-10T11:00:00Z",
        "processed_at": "2025-06-10T11:12:00Z",
    },
    {
        "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
        "title": "OSHA Process Safety Management Guidelines",
        "original_filename": "OSHA_PSM_Guidelines.pdf",
        "file_type": "pdf",
        "file_size": 12_456_000,
        "category": "regulation",
        "tags": ["osha", "psm", "safety", "regulation", "compliance"],
        "status": "ready",
        "processing_progress": 100.0,
        "chunk_count": 89,
        "uploaded_at": "2025-06-08T08:45:00Z",
        "processed_at": "2025-06-08T09:02:00Z",
    },
    {
        "id": "e5f6a7b8-c9d0-1234-efab-345678901234",
        "title": "Vibration Analysis Report — Compressor C-201",
        "original_filename": "Vibration_Analysis_C201.xlsx",
        "file_type": "xlsx",
        "file_size": 2_134_000,
        "category": "report",
        "tags": ["vibration", "compressor", "C-201", "analysis", "predictive"],
        "status": "ready",
        "processing_progress": 100.0,
        "chunk_count": 18,
        "uploaded_at": "2025-06-12T16:30:00Z",
        "processed_at": "2025-06-12T16:33:00Z",
    },
    {
        "id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
        "title": "Heat Exchanger E-301 Failure Investigation",
        "original_filename": "HX_E301_Failure_Report.pdf",
        "file_type": "pdf",
        "file_size": 5_678_000,
        "category": "report",
        "tags": ["heat-exchanger", "failure", "investigation", "E-301"],
        "status": "ready",
        "processing_progress": 100.0,
        "chunk_count": 34,
        "uploaded_at": "2025-06-11T10:15:00Z",
        "processed_at": "2025-06-11T10:22:00Z",
    },
]


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Upload a document for processing."""
    filename = file.filename or "Untitled"
    ext = f".{filename.split('.')[-1].lower()}" if "." in filename else ""
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    return {
        "id": str(uuid.uuid4()),
        "title": filename,
        "original_filename": filename,
        "file_type": ext.lstrip(".") if ext else "pdf",
        "file_size": 0,
        "status": "processing",
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("", response_model=PaginatedResponse)
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str | None = None,
    status: str | None = None,
    search: str | None = None,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """List documents with pagination and filtering."""
    items = DEMO_DOCUMENTS
    if category:
        items = [d for d in items if d["category"] == category]
    if status:
        items = [d for d in items if d["status"] == status]
    if search:
        items = [d for d in items if search.lower() in d["title"].lower()]

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
    }


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get document details by ID."""
    for doc in DEMO_DOCUMENTS:
        if doc["id"] == document_id:
            return {
                **doc,
                "extracted_text": "Sample extracted text from the document...",
                "metadata_json": {"pages": 42, "author": "Engineering Team"},
                "user_id": "demo-user-001",
            }
    return {**DEMO_DOCUMENTS[0], "user_id": "demo-user-001"}


@router.get("/{document_id}/chunks", response_model=list[ChunkResponse])
async def get_document_chunks(
    document_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """Get text chunks for a document."""
    return [
        {
            "id": str(uuid.uuid4()),
            "chunk_index": i,
            "content": f"Sample chunk {i} content from document {document_id}...",
            "token_count": 128,
            "embedding_id": f"emb_{document_id}_{i}",
        }
        for i in range(5)
    ]


@router.patch("/{document_id}", response_model=StatusResponse)
async def update_document(
    document_id: str,
    updates: DocumentUpdate,
    user: dict[str, Any] = Depends(get_current_user),
) -> StatusResponse:
    """Update document metadata."""
    return StatusResponse(status="ok", message="Document updated successfully")


@router.delete("/{document_id}", response_model=StatusResponse)
async def delete_document(
    document_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> StatusResponse:
    """Delete a document and all associated data."""
    return StatusResponse(status="ok", message="Document deleted successfully")


@router.get("/{document_id}/status")
async def get_document_status(
    document_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get document processing status."""
    return {
        "document_id": document_id,
        "status": "ready",
        "progress": 100.0,
        "steps": {
            "upload": "completed",
            "ocr": "completed",
            "text_extraction": "completed",
            "chunking": "completed",
            "embedding": "completed",
            "knowledge_graph": "completed",
        },
    }
