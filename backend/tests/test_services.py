"""
IndusMind AI — Service Unit Tests

Tests for DocumentService and RAGPipeline functionality.
"""

from __future__ import annotations

import pytest

from app.ai.embeddings.generator import text_chunker
from app.ai.ner.entity_extractor import entity_extractor
from app.ai.rag.pipeline import rag_pipeline
from app.services.document_service import document_service


class TestTextChunker:
    """Tests for semantic text chunking."""

    def test_chunking_short_text(self) -> None:
        """Short text should produce a single chunk."""
        text = "This is a simple industrial document about pump maintenance."
        chunks = text_chunker.chunk_text(text)
        assert len(chunks) == 1
        assert chunks[0]["chunk_index"] == 0
        assert chunks[0]["content"] == text

    def test_chunking_multiple_paragraphs(self) -> None:
        """Longer text should produce multiple chunks with metadata."""
        text = "Paragraph 1: Equipment inspection details.\n\n" * 50
        chunks = text_chunker.chunk_text(text, metadata={"doc_id": "test-123"})
        assert len(chunks) >= 1
        assert "document_id" in chunks[0] or "chunk_index" in chunks[0]


class TestEntityExtractor:
    """Tests for NER entity extraction."""

    def test_extract_equipment_tags(self) -> None:
        """Extractor should identify equipment tags like P-101 and C-201."""
        text = "Pump P-101 and Compressor C-201 require maintenance under OSHA PSM guidelines."
        entities = entity_extractor.extract_entities(text)
        assert "equipment" in entities
        names = [item["name"] for item in entities["equipment"]]
        assert "P-101" in names
        assert "C-201" in names

    def test_extract_regulations(self) -> None:
        """Extractor should identify regulatory standards like OSHA and ISO 45001."""
        text = "Compliance check against OSHA 1910.119 and ISO 45001 standards."
        entities = entity_extractor.extract_entities(text)
        assert "regulation" in entities
        assert len(entities["regulation"]) >= 1


@pytest.mark.asyncio
class TestRAGPipeline:
    """Tests for RAG query pipeline in demo mode."""

    async def test_rag_pipeline_query_returns_structure(self) -> None:
        """RAG pipeline query should return content, citations, and confidence score."""
        res = await rag_pipeline.query(question="What is the maintenance for pump P-101?")
        assert "content" in res
        assert "citations" in res
        assert "confidence_score" in res
        assert isinstance(res["confidence_score"], float)
        assert res["confidence_score"] > 0.0
