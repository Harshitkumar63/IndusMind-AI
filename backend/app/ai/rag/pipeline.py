"""
IndusMind AI — RAG Pipeline

Retrieval-Augmented Generation pipeline for industrial Q&A.
"""

from __future__ import annotations

from typing import Any

from app.ai.embeddings.generator import embedding_generator
from app.core.config import get_settings
from app.core.logging import get_logger
from app.infrastructure.llm import llm_gateway
from app.infrastructure.vector_store import vector_store

settings = get_settings()
logger = get_logger(__name__)

# System prompt for industrial Q&A
SYSTEM_PROMPT = """You are IndusMind AI, an expert industrial knowledge assistant.

Your role:
- Answer questions about industrial equipment, maintenance, safety, and compliance
- Always cite specific source documents when making claims
- Provide actionable recommendations
- Use technical language appropriate for engineers and plant managers
- If you're not sure about something, say so clearly

Format your responses with:
- Clear section headings (## Heading)
- Numbered findings
- Bullet-point recommendations
- A confidence score at the end

Always prioritize safety-related information."""


class RAGPipeline:
    """
    Full RAG pipeline: Query → Embed → Retrieve → Rerank → Generate → Cite

    Supports both demo mode (simulated) and production mode (real embeddings + LLM).
    """

    async def query(
        self,
        question: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute the full RAG pipeline for a user question.

        Returns:
            dict with: content, citations, confidence_score, suggested_questions, context_chunks
        """
        k = top_k or settings.TOP_K_RESULTS

        # Step 1: Generate query embedding
        query_embedding = embedding_generator.generate_single(question)

        # Step 2: Retrieve relevant chunks from vector store
        search_results = vector_store.query(
            query_embedding=query_embedding,
            n_results=k,
            where=filters,
        )

        # Step 3: Build context from retrieved chunks
        context_chunks = []
        if search_results["documents"] and search_results["documents"][0]:
            for i, doc_text in enumerate(search_results["documents"][0]):
                metadata = {}
                if search_results["metadatas"] and search_results["metadatas"][0]:
                    metadata = search_results["metadatas"][0][i]
                distance = 0.0
                if search_results["distances"] and search_results["distances"][0]:
                    distance = search_results["distances"][0][i]

                context_chunks.append({
                    "content": doc_text,
                    "metadata": metadata,
                    "distance": distance,
                    "relevance_score": max(0, 1 - distance),
                })

        # Step 4: Assemble context string
        context = self._build_context(context_chunks)

        # Step 5: Generate response with LLM
        response = await llm_gateway.generate_response(
            query=question,
            context=context,
            system_prompt=SYSTEM_PROMPT,
        )

        # Step 6: Build citations from retrieved chunks
        citations = self._build_citations(context_chunks)

        return {
            "content": response["content"],
            "citations": citations or response.get("citations", []),
            "confidence_score": response.get("confidence_score", 0.85),
            "suggested_questions": response.get("suggested_questions", []),
            "context_chunks": context_chunks,
        }

    def _build_context(self, chunks: list[dict[str, Any]]) -> str:
        """Build a context string from retrieved chunks."""
        if not chunks:
            return "No relevant documents found in the knowledge base."

        context_parts: list[str] = []
        for i, chunk in enumerate(chunks):
            source = chunk["metadata"].get("document_title", f"Source {i + 1}")
            context_parts.append(
                f"[Source {i + 1}: {source}]\n{chunk['content']}\n"
            )
        return "\n---\n".join(context_parts)

    def _build_citations(self, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build citation objects from context chunks."""
        citations = []
        for chunk in chunks:
            if chunk.get("relevance_score", 0) > 0.5:
                citations.append({
                    "document_id": chunk["metadata"].get("document_id", ""),
                    "document_title": chunk["metadata"].get("document_title", "Unknown"),
                    "chunk_id": chunk["metadata"].get("chunk_id", ""),
                    "chunk_content": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
                    "relevance_score": round(chunk["relevance_score"], 3),
                })
        return citations


# Singleton
rag_pipeline = RAGPipeline()
