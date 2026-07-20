"""
IndusMind AI — Vector Store Infrastructure

ChromaDB client for document embedding storage and similarity search.
"""

from __future__ import annotations

import uuid
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class VectorStore:
    """ChromaDB vector store for document embeddings and semantic search."""

    def __init__(self) -> None:
        self._client: Any = None
        self._collection: Any = None

    async def connect(self) -> None:
        """Initialize ChromaDB connection."""
        if settings.DEMO_MODE:
            logger.info("VectorStore: Running in demo mode")
            return
        try:
            import chromadb

            self._client = chromadb.HttpClient(
                host=settings.CHROMA_HOST,
                port=settings.CHROMA_PORT,
            )
            self._collection = self._client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(
                "VectorStore: Connected to ChromaDB",
                collection=settings.CHROMA_COLLECTION,
                count=self._collection.count(),
            )
        except Exception as e:
            logger.warning("VectorStore: Connection failed", error=str(e))

    def add_embeddings(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """Add document embeddings to the vector store."""
        if not self._collection:
            logger.debug("VectorStore: Skipped add (no collection)")
            return
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        query_embedding: list[float],
        n_results: int = 10,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Query similar documents by embedding vector."""
        if not self._collection:
            return {"ids": [[]], "distances": [[]], "documents": [[]], "metadatas": [[]]}
        params: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,
        }
        if where:
            params["where"] = where
        return self._collection.query(**params)

    def delete_by_document(self, document_id: str) -> None:
        """Delete all embeddings for a specific document."""
        if not self._collection:
            return
        self._collection.delete(where={"document_id": document_id})

    def get_count(self) -> int:
        """Get total number of embeddings."""
        if not self._collection:
            return 0
        return self._collection.count()


# Singleton
vector_store = VectorStore()
