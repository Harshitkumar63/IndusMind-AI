"""
IndusMind AI — Chat / AI Service

Manages conversations and RAG-powered question answering.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from app.ai.rag.pipeline import rag_pipeline
from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


# ─── In-memory store for demo mode ──────────────────────────

_demo_conversations: dict[str, dict[str, Any]] = {}


class ChatService:
    """Manages AI conversations and RAG-powered Q&A."""

    async def create_conversation(
        self,
        title: str | None = None,
        user_id: str = "demo_user",
    ) -> dict[str, Any]:
        """Create a new conversation."""
        conv_id = str(uuid.uuid4())
        conversation = {
            "id": conv_id,
            "title": title or "New Conversation",
            "user_id": user_id,
            "messages": [],
            "message_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_message_at": datetime.now(timezone.utc).isoformat(),
        }
        _demo_conversations[conv_id] = conversation
        return conversation

    async def list_conversations(self, user_id: str = "demo_user") -> list[dict[str, Any]]:
        """List all conversations for a user."""
        return [
            {k: v for k, v in conv.items() if k != "messages"}
            for conv in _demo_conversations.values()
            if conv["user_id"] == user_id
        ]

    async def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        """Get a conversation with its messages."""
        return _demo_conversations.get(conversation_id)

    async def send_message(
        self,
        conversation_id: str,
        content: str,
        user_id: str = "demo_user",
    ) -> dict[str, Any]:
        """
        Send a message in a conversation and get an AI response.

        Pipeline: User Message → RAG Query → AI Response with Citations
        """
        conversation = _demo_conversations.get(conversation_id)
        if not conversation:
            # Auto-create
            conversation = await self.create_conversation(title=content[:50], user_id=user_id)

        # Add user message
        user_msg = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        conversation["messages"].append(user_msg)
        conversation["message_count"] += 1

        # RAG pipeline
        logger.info("Processing chat query", conversation_id=conversation_id, query_length=len(content))
        rag_result = await rag_pipeline.query(question=content)

        # Add AI message
        ai_msg = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": rag_result["content"],
            "citations": rag_result["citations"],
            "confidence_score": rag_result["confidence_score"],
            "suggested_questions": rag_result["suggested_questions"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        conversation["messages"].append(ai_msg)
        conversation["message_count"] += 1
        conversation["last_message_at"] = ai_msg["created_at"]

        # Auto-title from first message
        if conversation["title"] == "New Conversation" and len(conversation["messages"]) == 2:
            conversation["title"] = content[:60] + ("..." if len(content) > 60 else "")

        return ai_msg

    async def delete_conversation(self, conversation_id: str) -> None:
        """Delete a conversation."""
        _demo_conversations.pop(conversation_id, None)


# Singleton
chat_service = ChatService()
