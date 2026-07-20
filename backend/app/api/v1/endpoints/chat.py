"""
IndusMind AI — AI Chat Endpoints

Conversation management and RAG-powered chat with citations.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user
from app.schemas import (
    ConversationCreate,
    ConversationDetailResponse,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    StatusResponse,
)

router = APIRouter()

# ─── Demo Conversations ──────────────────────────────────────

DEMO_CONVERSATIONS: list[dict] = [
    {
        "id": "conv-001",
        "title": "Pump P-101 Maintenance Query",
        "context_type": "equipment",
        "message_count": 4,
        "last_message_at": "2025-06-15T10:30:00Z",
        "created_at": "2025-06-15T10:00:00Z",
    },
    {
        "id": "conv-002",
        "title": "OSHA Compliance Check",
        "context_type": "compliance",
        "message_count": 6,
        "last_message_at": "2025-06-14T15:45:00Z",
        "created_at": "2025-06-14T14:30:00Z",
    },
    {
        "id": "conv-003",
        "title": "Boiler Inspection Findings",
        "context_type": "document",
        "message_count": 3,
        "last_message_at": "2025-06-13T09:20:00Z",
        "created_at": "2025-06-13T09:00:00Z",
    },
]

DEMO_AI_RESPONSES: dict[str, dict] = {
    "default": {
        "content": (
            "Based on the analysis of your uploaded documents, here is what I found:\n\n"
            "## Key Findings\n\n"
            "1. **Pump P-101** has a documented maintenance schedule requiring quarterly "
            "vibration analysis and annual overhaul per the manufacturer's manual (Section 4.2).\n\n"
            "2. The last recorded maintenance was performed on **March 15, 2025**, which means "
            "the next quarterly check is due by **June 15, 2025**.\n\n"
            "3. According to the vibration analysis report from April 2025, bearing vibration "
            "levels were at **4.2 mm/s RMS**, which is within the acceptable range (< 7.1 mm/s) "
            "per ISO 10816-3.\n\n"
            "## Recommendations\n\n"
            "- Schedule the quarterly vibration check before the deadline\n"
            "- Monitor bearing temperature trends — a 3°C increase was noted in the last reading\n"
            "- Review the seal flush system as mentioned in Maintenance Advisory MA-2025-012\n\n"
            "*Confidence: 92% — Based on 3 source documents*"
        ),
        "confidence_score": 0.92,
        "citations": [
            {
                "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "document_title": "Centrifugal Pump P-101 Maintenance Manual",
                "chunk_id": "chunk-001",
                "chunk_content": "Section 4.2: Quarterly maintenance shall include vibration analysis...",
                "relevance_score": 0.95,
            },
            {
                "document_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
                "document_title": "Vibration Analysis Report — Compressor C-201",
                "chunk_id": "chunk-002",
                "chunk_content": "Bearing vibration measured at 4.2 mm/s RMS, within ISO 10816-3 limits...",
                "relevance_score": 0.88,
            },
        ],
        "suggested_questions": [
            "What is the recommended bearing replacement interval for P-101?",
            "Show me all maintenance records for P-101 in the last 12 months",
            "What are the ISO 10816-3 vibration severity limits?",
            "Are there any pending work orders for pump P-101?",
        ],
    },
}


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    data: ConversationCreate,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Create a new chat conversation."""
    return {
        "id": str(uuid.uuid4()),
        "title": data.title or "New Conversation",
        "context_type": data.context_type,
        "message_count": 0,
        "last_message_at": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    user: dict[str, Any] = Depends(get_current_user),
) -> list[dict]:
    """List all conversations for the current user."""
    return DEMO_CONVERSATIONS


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Get conversation with full message history."""
    return {
        "id": conversation_id,
        "title": "Pump P-101 Maintenance Query",
        "context_type": "equipment",
        "message_count": 2,
        "last_message_at": datetime.now(timezone.utc).isoformat(),
        "created_at": "2025-06-15T10:00:00Z",
        "messages": [
            {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": "What is the maintenance schedule for pump P-101?",
                "citations": None,
                "confidence_score": None,
                "suggested_questions": None,
                "created_at": "2025-06-15T10:00:00Z",
            },
            {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": DEMO_AI_RESPONSES["default"]["content"],
                "citations": DEMO_AI_RESPONSES["default"]["citations"],
                "confidence_score": DEMO_AI_RESPONSES["default"]["confidence_score"],
                "suggested_questions": DEMO_AI_RESPONSES["default"]["suggested_questions"],
                "created_at": "2025-06-15T10:00:05Z",
            },
        ],
    }


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: str,
    data: MessageCreate,
    user: dict[str, Any] = Depends(get_current_user),
) -> dict:
    """Send a message and get an AI response."""
    response = DEMO_AI_RESPONSES["default"]
    return {
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": response["content"],
        "citations": response["citations"],
        "confidence_score": response["confidence_score"],
        "suggested_questions": response["suggested_questions"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@router.delete("/conversations/{conversation_id}", response_model=StatusResponse)
async def delete_conversation(
    conversation_id: str,
    user: dict[str, Any] = Depends(get_current_user),
) -> StatusResponse:
    """Delete a conversation."""
    return StatusResponse(status="ok", message="Conversation deleted successfully")
