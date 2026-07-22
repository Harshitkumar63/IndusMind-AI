# AI Pipeline

> Document intelligence and RAG pipeline architecture for IndusMind AI

---

## Overview

The IndusMind AI pipeline transforms raw industrial documents into structured, queryable intelligence through a multi-stage processing pipeline.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Document │───▶│   OCR/   │───▶│ Semantic │───▶│Embedding │───▶│ Vector   │
│  Upload  │    │  Extract │    │ Chunking │    │Generation│    │ Storage  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │                                              │
                     ▼                                              ▼
                ┌──────────┐                                   ┌──────────┐
                │   NER    │                                   │  Query   │
                │ Entity   │                                   │Embedding │
                │Extraction│                                   └────┬─────┘
                └────┬─────┘                                        │
                     │                                              ▼
                     ▼                                         ┌──────────┐
                ┌──────────┐                                   │ Retrieve │
                │Knowledge │                                   │  Top-K   │
                │  Graph   │                                   └────┬─────┘
                │  (Neo4j) │                                        │
                └──────────┘                                        ▼
                                                               ┌──────────┐
                                                               │ Context  │
                                                               │ Assembly │
                                                               └────┬─────┘
                                                                    │
                                                                    ▼
                                                               ┌──────────┐
                                                               │   LLM    │
                                                               │Generation│
                                                               └────┬─────┘
                                                                    │
                                                                    ▼
                                                               ┌──────────┐
                                                               │Response +│
                                                               │Citations │
                                                               └──────────┘
```

---

## Stage 1: Document Ingestion

### Supported Formats

| Format | Library | Method |
|--------|---------|--------|
| PDF (native text) | PyMuPDF (`fitz`) | Direct text extraction per page |
| PDF (scanned/image) | Tesseract OCR | Image-to-text conversion |
| DOCX | python-docx | Paragraph extraction |
| XLSX/CSV | openpyxl / csv | Row-by-row text conversion |
| Images (PNG, JPG) | Tesseract OCR | Full-page OCR |

### Implementation

```python
# backend/app/ai/ocr/extractor.py

class DocumentExtractor:
    """Multi-format document text extraction."""

    def extract(self, file_path: str, file_type: str) -> ExtractedDocument:
        """Route to the appropriate extraction method."""
        ...

    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF with OCR fallback."""
        ...
```

### Processing Flow

1. File uploaded via API → saved to storage
2. Celery worker picks up processing task
3. Format detected → appropriate extractor invoked
4. Raw text extracted with page numbers
5. Metadata recorded in PostgreSQL

---

## Stage 2: Semantic Chunking

### Strategy

IndusMind AI uses **sentence-boundary-aware chunking** to preserve semantic coherence:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHUNK_SIZE` | 512 tokens | Target chunk size |
| `CHUNK_OVERLAP` | 50 tokens | Overlap between consecutive chunks |

### Algorithm

1. Split text into sentences using punctuation boundaries
2. Accumulate sentences until `CHUNK_SIZE` is reached
3. Create chunk with `CHUNK_OVERLAP` tokens from the previous chunk
4. Record chunk metadata (page number, position, token count)

```python
# backend/app/ai/embeddings/generator.py

def chunk_text(self, text: str) -> list[TextChunk]:
    """Split text into overlapping semantic chunks."""
    ...
```

---

## Stage 3: Embedding Generation

### Models

| Model | Dimensions | Use Case |
|-------|-----------|----------|
| `all-MiniLM-L6-v2` | 384 | Default local model (fast, free) |
| `text-embedding-3-small` | 1536 | OpenAI cloud model (higher quality) |

### Process

1. Each chunk is encoded into a dense vector
2. Vectors are stored in ChromaDB with metadata
3. Batch processing for efficiency (16 chunks per batch)

```python
def generate_embeddings(self, chunks: list[TextChunk]) -> list[list[float]]:
    """Generate embedding vectors for text chunks."""
    ...
```

---

## Stage 4: Vector Storage (ChromaDB)

### Collection Configuration

```python
collection = client.get_or_create_collection(
    name="indusmind_documents",
    metadata={"hnsw:space": "cosine"}  # Cosine similarity
)
```

### Stored Metadata

Each vector entry includes:
- `document_id` — Parent document UUID
- `document_title` — Human-readable title
- `chunk_index` — Position within document
- `page_number` — Source page
- `category` — Document category
- `file_type` — Original file format

---

## Stage 5: Named Entity Recognition (NER)

### Entity Types

| Entity | Pattern | Examples |
|--------|---------|----------|
| Equipment ID | `[A-Z]-\d{3}` pattern | P-101, C-201, B-401 |
| SOP Reference | `SOP-\d+` pattern | SOP-2025-001 |
| Regulation | Standard codes | OSHA 1910.119, ISO 45001, API 510 |
| Incident | `INC-\d+` pattern | INC-2025-042 |
| Location | Named areas | Unit-1, Building A, Control Room |
| Person | Named individuals | From document metadata |

### Implementation

```python
# backend/app/ai/ner/entity_extractor.py

class IndustrialNERExtractor:
    """Regex-based entity extraction for industrial documents."""

    PATTERNS = {
        "equipment": r"[A-Z]{1,3}-\d{2,4}[A-Z]?",
        "sop": r"SOP[-\s]?\d{4}[-\s]?\d{2,4}",
        "regulation": r"(OSHA|ISO|API|ASME)\s*\d+[\.\-]?\d*",
        ...
    }
```

### Knowledge Graph Construction

Extracted entities are connected in Neo4j based on **co-occurrence analysis**:

1. Entities appearing in the same document section are linked
2. Relationship weight = frequency of co-occurrence
3. Relationship type inferred from entity type pairs

---

## Stage 6: RAG Query Pipeline

### Full Pipeline Flow

```python
# backend/app/ai/rag/pipeline.py

class RAGPipeline:
    async def query(self, question: str, top_k: int = 10) -> dict:
        # 1. Generate query embedding
        query_embedding = embedding_generator.generate_single(question)

        # 2. Retrieve relevant chunks from vector store
        results = vector_store.query(query_embedding, n_results=top_k)

        # 3. Build context from retrieved chunks
        context = self._build_context(results)

        # 4. Generate response with LLM
        response = await llm_gateway.generate_response(
            query=question,
            context=context,
            system_prompt=SYSTEM_PROMPT,
        )

        # 5. Build citations from retrieved chunks
        citations = self._build_citations(results)

        return {
            "content": response["content"],
            "citations": citations,
            "confidence_score": response["confidence_score"],
            "suggested_questions": response["suggested_questions"],
        }
```

### System Prompt

The RAG pipeline uses a specialized system prompt for industrial Q&A:

```
You are IndusMind AI, an expert industrial knowledge assistant.

Your role:
- Answer questions about industrial equipment, maintenance, safety, and compliance
- Always cite specific source documents when making claims
- Provide actionable recommendations
- Use technical language appropriate for engineers and plant managers
- If you're not sure about something, say so clearly

Always prioritize safety-related information.
```

### LLM Gateway

The `LLMGateway` provides a unified interface with automatic demo fallback:

| Mode | Behavior |
|------|----------|
| **Production** | Routes to OpenAI GPT-4o API |
| **Demo** | Returns curated responses based on query keywords |

Demo mode detects query intent via keyword matching and returns domain-specific responses for maintenance, compliance, and general queries — complete with realistic citations.

---

## Configuration

All pipeline parameters are configurable via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHUNK_SIZE` | 512 | Target tokens per chunk |
| `CHUNK_OVERLAP` | 50 | Overlap tokens between chunks |
| `TOP_K_RESULTS` | 10 | Number of chunks to retrieve |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Local embedding model |
| `OPENAI_MODEL` | `gpt-4o` | LLM model for generation |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | Cloud embedding model |
| `DEMO_MODE` | `true` | Use demo responses |

---

## Related Documentation

- [Architecture](ARCHITECTURE.md)
- [Knowledge Graph](KNOWLEDGE_GRAPH.md)
- [API Reference](API.md)
- [Database Design](DATABASE.md)
