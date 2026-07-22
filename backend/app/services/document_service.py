"""
IndusMind AI — Document Service

Handles document upload, processing orchestration, and CRUD operations.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from app.ai.embeddings.generator import embedding_generator, text_chunker
from app.ai.ner.entity_extractor import entity_extractor
from app.ai.ocr.extractor import document_extractor
from app.core.config import get_settings
from app.core.logging import get_logger
from app.infrastructure.storage import file_storage
from app.infrastructure.vector_store import vector_store

settings = get_settings()
logger = get_logger(__name__)


class DocumentService:
    """Orchestrates the full document ingestion pipeline."""

    async def upload_document(
        self,
        filename: str,
        content: bytes,
        file_type: str,
        uploaded_by: str = "demo_user",
    ) -> dict[str, Any]:
        """
        Process a new document upload:
        1. Save file to storage
        2. Extract text (OCR/parser)
        3. Chunk text
        4. Generate embeddings
        5. Store in vector DB
        6. Extract entities for knowledge graph
        """
        document_id = str(uuid.uuid4())
        logger.info("Starting document ingestion", document_id=document_id, filename=filename)

        # Step 1: Save to storage
        file_path = await file_storage.save_file(content, filename, document_id)

        # Step 2: Extract text
        extraction = await document_extractor.extract(file_path)
        full_text = extraction["text"]
        page_count = extraction.get("page_count", 0)
        doc_metadata = extraction.get("metadata", {})

        # Step 3: Save extracted text
        await file_storage.save_extracted_text(document_id, full_text)

        # Step 4: Chunk text
        chunks = text_chunker.chunk_text(
            full_text,
            metadata={
                "document_id": document_id,
                "document_title": filename,
                "file_type": file_type,
            },
        )

        # Step 5: Generate embeddings & store
        if chunks:
            chunk_texts = [c["content"] for c in chunks]
            chunk_ids = [f"{document_id}_chunk_{c['chunk_index']}" for c in chunks]
            embeddings = embedding_generator.generate(chunk_texts)
            metadatas = [
                {
                    "document_id": document_id,
                    "document_title": filename,
                    "chunk_index": c["chunk_index"],
                    "token_count": c["token_count"],
                }
                for c in chunks
            ]
            vector_store.add_embeddings(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=chunk_texts,
                metadatas=metadatas,
            )

        # Step 6: Extract entities
        entities = entity_extractor.extract_entities(full_text)
        relationships = entity_extractor.extract_relationships(entities, full_text)

        result = {
            "id": document_id,
            "filename": filename,
            "file_type": file_type,
            "file_path": file_path,
            "status": "ready",
            "page_count": page_count,
            "chunk_count": len(chunks),
            "char_count": len(full_text),
            "entity_count": sum(len(v) for v in entities.values()),
            "relationship_count": len(relationships),
            "metadata": doc_metadata,
            "entities": entities,
            "relationships": relationships,
            "uploaded_by": uploaded_by,
            "uploaded_at": datetime.now(UTC).isoformat(),
        }

        logger.info(
            "Document ingestion complete",
            document_id=document_id,
            chunks=len(chunks),
            entities=result["entity_count"],
        )
        return result

    async def delete_document(self, document_id: str) -> None:
        """Delete a document and all associated data."""
        await file_storage.delete_document_files(document_id)
        vector_store.delete_by_document(document_id)
        logger.info("Document deleted", document_id=document_id)

    async def get_document_chunks(self, document_id: str) -> list[dict[str, Any]]:
        """Retrieve all chunks for a document from the vector store."""
        results = vector_store.query(
            query_embedding=[0.0] * 384,  # Dummy — just for retrieval by metadata
            n_results=100,
            where={"document_id": document_id},
        )
        chunks = []
        if results["documents"] and results["documents"][0]:
            for i, text in enumerate(results["documents"][0]):
                chunks.append(
                    {
                        "content": text,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    }
                )
        return chunks


# Singleton
document_service = DocumentService()
