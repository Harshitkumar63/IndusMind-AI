"""
IndusMind AI — LLM Gateway

Unified interface for LLM interactions (OpenAI, with extensibility for others).
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from app.core.config import get_settings
from app.core.exceptions import AIServiceError
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


# ─── Demo Responses ─────────────────────────────────────────

DEMO_RESPONSES: dict[str, str] = {
    "default": (
        "Based on the analysis of your uploaded documents, I found several relevant sections:\n\n"
        "## Key Findings\n\n"
        "1. **Equipment Maintenance**: The maintenance manual specifies quarterly vibration analysis "
        "and annual overhaul procedures for all critical rotating equipment.\n\n"
        "2. **Safety Compliance**: Current operations are largely aligned with OSHA PSM requirements, "
        "with minor gaps in mechanical integrity documentation.\n\n"
        "3. **Risk Assessment**: Based on historical incident data and maintenance records, "
        "the overall equipment reliability index stands at 94.2%.\n\n"
        "## Recommendations\n\n"
        "- Schedule overdue predictive maintenance tasks\n"
        "- Update piping inspection records for Unit-1\n"
        "- Review emergency response procedures per latest OSHA guidelines\n\n"
        "*Confidence: 89% — Based on 4 source documents*"
    ),
    "maintenance": (
        "## Maintenance Analysis\n\n"
        "Based on maintenance records and equipment specifications:\n\n"
        "1. **Pump P-101** requires quarterly vibration analysis (ISO 10816-3 standard). "
        "Last analysis showed 4.2 mm/s RMS — within Zone B acceptable limits.\n\n"
        "2. **Compressor C-201** has overdue valve plate inspection. "
        "Vibration trending shows increasing 1x RPM amplitude suggesting imbalance.\n\n"
        "3. **Boiler B-401** safety valve SV-401A needs immediate inspection — "
        "failure probability estimated at 55% within 30-45 days.\n\n"
        "### Priority Actions\n"
        "- URGENT: Inspect B-401 safety valve within 48 hours\n"
        "- HIGH: Schedule C-201 valve plate inspection\n"
        "- MEDIUM: Plan P-101 seal replacement at next shutdown\n\n"
        "*Confidence: 91% — Based on 5 source documents*"
    ),
    "compliance": (
        "## Compliance Assessment\n\n"
        "After reviewing your documents against regulatory requirements:\n\n"
        "### Overall Score: 81.6%\n\n"
        "| Standard | Score | Status |\n"
        "|----------|-------|--------|\n"
        "| API 510 | 95% | ✅ Compliant |\n"
        "| ISO 45001 | 88% | ✅ Compliant |\n"
        "| OSHA PSM | 85% | ✅ Compliant |\n"
        "| ISO 14001 | 55% | ❌ Non-Compliant |\n\n"
        "### Critical Gaps\n"
        "1. **Environmental Monitoring**: Missing air emission data for Q1 2025\n"
        "2. **Hazardous Waste**: Storage exceeding 90-day regulatory limit\n"
        "3. **Mechanical Integrity**: Piping inspection schedule behind by 25 days\n\n"
        "*Confidence: 87% — Based on 6 source documents*"
    ),
}

DEMO_CITATIONS = [
    {
        "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "document_title": "Centrifugal Pump P-101 Maintenance Manual",
        "chunk_id": "chunk-001",
        "chunk_content": "Section 4.2: Quarterly maintenance includes vibration analysis, bearing temperature, and seal inspection...",
        "relevance_score": 0.95,
    },
    {
        "document_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "document_title": "Annual Boiler Inspection Report 2025",
        "chunk_id": "chunk-002",
        "chunk_content": "Safety valve SV-401A showed signs of seat erosion during visual inspection...",
        "relevance_score": 0.88,
    },
    {
        "document_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
        "document_title": "OSHA Process Safety Management Guidelines",
        "chunk_id": "chunk-003",
        "chunk_content": "Mechanical integrity program shall include inspection and testing of process equipment...",
        "relevance_score": 0.82,
    },
]

DEMO_SUGGESTIONS = [
    "What is the recommended bearing replacement interval for P-101?",
    "Show me all maintenance records for P-101 in the last 12 months",
    "What are the ISO 10816-3 vibration severity limits?",
    "Compare our compliance with OSHA PSM Section 1910.119(j)",
]


class LLMGateway:
    """Unified LLM interface — supports OpenAI with demo mode fallback."""

    def __init__(self) -> None:
        self._client: Any = None

    async def initialize(self) -> None:
        """Initialize the LLM client."""
        if settings.DEMO_MODE:
            logger.info("LLM Gateway: Running in demo mode")
            return
        try:
            from openai import AsyncOpenAI

            self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("LLM Gateway: OpenAI client initialized", model=settings.OPENAI_MODEL)
        except Exception as e:
            logger.warning("LLM Gateway: Failed to initialize", error=str(e))

    async def generate_response(
        self,
        query: str,
        context: str = "",
        system_prompt: str = "",
    ) -> dict[str, Any]:
        """
        Generate an AI response for a user query.

        Returns dict with: content, citations, confidence_score, suggested_questions
        """
        if settings.DEMO_MODE or not self._client:
            return self._generate_demo_response(query)

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if context:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Use the following context to answer the question. "
                        f"Always cite your sources.\n\nContext:\n{context}",
                    }
                )
            messages.append({"role": "user", "content": query})

            response = await self._client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=2000,
            )
            content = response.choices[0].message.content or ""
            return {
                "content": content,
                "citations": [],
                "confidence_score": 0.85,
                "suggested_questions": [],
            }
        except Exception as e:
            logger.error("LLM generation failed", error=str(e))
            raise AIServiceError(f"LLM generation failed: {e}")

    async def generate_stream(
        self,
        query: str,
        context: str = "",
        system_prompt: str = "",
    ) -> AsyncGenerator[str, None]:
        """Stream response tokens for real-time chat."""
        if settings.DEMO_MODE or not self._client:
            response = self._generate_demo_response(query)
            for word in response["content"].split(" "):
                yield word + " "
            return

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if context:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Context:\n{context}",
                    }
                )
            messages.append({"role": "user", "content": query})

            stream = await self._client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=2000,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content
        except Exception as e:
            logger.error("LLM streaming failed", error=str(e))
            yield f"\n\n*Error: {e}*"

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of text chunks."""
        if settings.DEMO_MODE or not self._client:
            import random

            return [[random.uniform(-1, 1) for _ in range(384)] for _ in texts]

        try:
            response = await self._client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=texts,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise AIServiceError(f"Embedding generation failed: {e}")

    def _generate_demo_response(self, query: str) -> dict[str, Any]:
        """Generate a contextual demo response based on query keywords."""
        query_lower = query.lower()

        if any(kw in query_lower for kw in ["maintenance", "repair", "failure", "pump", "bearing", "vibration"]):
            content = DEMO_RESPONSES["maintenance"]
        elif any(kw in query_lower for kw in ["compliance", "osha", "iso", "regulation", "audit", "violation"]):
            content = DEMO_RESPONSES["compliance"]
        else:
            content = DEMO_RESPONSES["default"]

        return {
            "content": content,
            "citations": DEMO_CITATIONS,
            "confidence_score": 0.89,
            "suggested_questions": DEMO_SUGGESTIONS,
        }


# Singleton
llm_gateway = LLMGateway()
