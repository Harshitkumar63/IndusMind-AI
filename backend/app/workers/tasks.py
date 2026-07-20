"""
IndusMind AI — Celery Worker Tasks

Async background tasks for document processing, embedding generation,
and knowledge graph extraction.
"""

from __future__ import annotations

import asyncio
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

# ─── Celery Configuration ───────────────────────────────────
# Note: In demo mode, tasks run synchronously.
# In production, use: celery -A app.workers.tasks worker -l info

try:
    from celery import Celery

    celery_app = Celery(
        "indusmind",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
    )
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=600,
        task_soft_time_limit=300,
        worker_prefetch_multiplier=1,
    )
except ImportError:
    celery_app = None
    logger.info("Celery not available — tasks will run synchronously")


def _run_async(coro: Any) -> Any:
    """Helper to run async functions from sync Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ─── Task Definitions ───────────────────────────────────────

def process_document_task(
    file_path: str,
    document_id: str,
    filename: str,
    file_type: str,
) -> dict[str, Any]:
    """
    Background task: Full document processing pipeline.

    1. Extract text (OCR/parser)
    2. Chunk into semantic segments
    3. Generate embeddings
    4. Store in vector database
    5. Extract entities (NER)
    6. Build knowledge graph relationships
    """
    from app.ai.embeddings.generator import embedding_generator, text_chunker
    from app.ai.ner.entity_extractor import entity_extractor
    from app.ai.ocr.extractor import document_extractor
    from app.infrastructure.storage import file_storage
    from app.infrastructure.vector_store import vector_store

    logger.info("Background task: Processing document", document_id=document_id)

    # Extract text
    extraction = _run_async(document_extractor.extract(file_path))
    full_text = extraction["text"]
    page_count = extraction.get("page_count", 0)

    # Save extracted text
    _run_async(file_storage.save_extracted_text(document_id, full_text))

    # Chunk
    chunks = text_chunker.chunk_text(
        full_text,
        metadata={
            "document_id": document_id,
            "document_title": filename,
            "file_type": file_type,
        },
    )

    # Embed + store
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

    # NER
    entities = entity_extractor.extract_entities(full_text)
    relationships = entity_extractor.extract_relationships(entities, full_text)

    result = {
        "document_id": document_id,
        "status": "ready",
        "page_count": page_count,
        "chunk_count": len(chunks),
        "char_count": len(full_text),
        "entity_count": sum(len(v) for v in entities.values()),
        "relationship_count": len(relationships),
    }

    logger.info("Background task: Document processed", **result)
    return result


def rebuild_embeddings_task(document_id: str) -> dict[str, Any]:
    """Re-generate embeddings for a previously processed document."""
    from app.infrastructure.storage import file_storage
    from app.infrastructure.vector_store import vector_store
    from app.ai.embeddings.generator import embedding_generator, text_chunker

    logger.info("Rebuilding embeddings", document_id=document_id)

    # Delete old embeddings
    vector_store.delete_by_document(document_id)

    # Read extracted text
    text_path = f"uploads/extracted/{document_id}.txt"
    try:
        text = _run_async(file_storage.read_file(text_path)).decode("utf-8")
    except Exception:
        return {"status": "error", "message": "Extracted text not found"}

    # Re-chunk and re-embed
    chunks = text_chunker.chunk_text(text, metadata={"document_id": document_id})
    if chunks:
        chunk_texts = [c["content"] for c in chunks]
        chunk_ids = [f"{document_id}_chunk_{c['chunk_index']}" for c in chunks]
        embeddings = embedding_generator.generate(chunk_texts)
        metadatas = [{"document_id": document_id, "chunk_index": c["chunk_index"]} for c in chunks]
        vector_store.add_embeddings(ids=chunk_ids, embeddings=embeddings, documents=chunk_texts, metadatas=metadatas)

    return {"status": "completed", "chunks_rebuilt": len(chunks)}


# Register with Celery if available
if celery_app:
    process_document_task = celery_app.task(name="process_document")(process_document_task)
    rebuild_embeddings_task = celery_app.task(name="rebuild_embeddings")(rebuild_embeddings_task)
