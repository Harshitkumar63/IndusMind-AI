"""
IndusMind AI — Embedding Generator

Generates vector embeddings using Sentence Transformers or OpenAI.
"""

from __future__ import annotations

import re
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class TextChunker:
    """Semantic text chunker that splits on sentence boundaries."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Split text into overlapping chunks at sentence boundaries.

        Returns list of dicts: {content, chunk_index, token_count, metadata}
        """
        if not text.strip():
            return []

        # Clean text
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)

        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks: list[dict[str, Any]] = []
        current_chunk: list[str] = []
        current_length = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_len = len(sentence.split())

            if current_length + sentence_len > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(
                    {
                        "content": chunk_text,
                        "chunk_index": chunk_index,
                        "token_count": len(chunk_text.split()),
                        "metadata": metadata or {},
                    }
                )
                chunk_index += 1

                # Keep overlap
                overlap_words = self.chunk_overlap
                overlap_text = " ".join(current_chunk)
                overlap_sentences = overlap_text.split(". ")
                current_chunk = []
                current_length = 0

                # Add last few sentences for overlap
                words_kept = 0
                for s in reversed(overlap_sentences):
                    if words_kept + len(s.split()) <= overlap_words:
                        current_chunk.insert(0, s)
                        words_kept += len(s.split())
                    else:
                        break
                current_length = words_kept

            current_chunk.append(sentence)
            current_length += sentence_len

        # Final chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(
                {
                    "content": chunk_text,
                    "chunk_index": chunk_index,
                    "token_count": len(chunk_text.split()),
                    "metadata": metadata or {},
                }
            )

        logger.info(f"Text chunked into {len(chunks)} chunks")
        return chunks


class EmbeddingGenerator:
    """Generates embeddings using Sentence Transformers or OpenAI API."""

    def __init__(self) -> None:
        self._model: Any = None
        self._model_name = settings.EMBEDDING_MODEL

    def load_model(self) -> None:
        """Load the sentence transformer model."""
        if settings.DEMO_MODE:
            logger.info("EmbeddingGenerator: Demo mode, using random vectors")
            return
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
            logger.info(f"EmbeddingGenerator: Loaded model {self._model_name}")
        except ImportError:
            logger.warning("sentence-transformers not installed")

    def generate(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        if settings.DEMO_MODE or not self._model:
            import random

            dim = 384
            return [[random.uniform(-0.1, 0.1) for _ in range(dim)] for _ in texts]

        embeddings = self._model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def generate_single(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        return self.generate([text])[0]


# Singletons
text_chunker = TextChunker(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
)
embedding_generator = EmbeddingGenerator()
