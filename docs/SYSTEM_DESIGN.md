# System Design

> High-level system design and scalability considerations for IndusMind AI

---

## Problem Statement

Industrial organizations generate thousands of documents — maintenance manuals, inspection reports, SOPs, compliance records — but this knowledge is trapped in PDFs and spreadsheets. Engineers waste hours searching for answers that exist somewhere in the document corpus.

**IndusMind AI solves this by:**
1. Ingesting and understanding industrial documents at scale
2. Enabling natural language Q&A with source citations
3. Building a knowledge graph of entities and relationships
4. Providing predictive maintenance and compliance intelligence

---

## System Context

```
                    ┌─────────────────┐
                    │   Industrial    │
                    │    Engineer     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   IndusMind AI  │
                    │    Platform     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐  ┌─────▼─────┐  ┌────▼────────┐
     │  Documents  │  │  External │  │  Monitoring  │
     │  (PDFs,     │  │  LLM API  │  │   Systems    │
     │   SOPs,     │  │  (OpenAI) │  │   (SCADA,    │
     │   Reports)  │  └───────────┘  │    Sensors)  │
     └─────────────┘                 └──────────────┘
```

---

## Core Design Decisions

### 1. Demo Mode Architecture

**Decision**: Implement a full demo mode that works without any external API keys.

**Rationale**: For hackathon evaluation and recruiter demos, the platform must work instantly without requiring OpenAI keys, database setup, or Docker. The frontend operates with hardcoded demo data, and the backend LLM Gateway falls back to curated domain-specific responses.

### 2. Polyglot Persistence

**Decision**: Use three specialized databases instead of one general-purpose database.

| Database | Optimized For |
|----------|--------------|
| PostgreSQL | ACID transactions, relational queries, metadata |
| ChromaDB | High-dimensional vector similarity search |
| Neo4j | Graph traversal, relationship queries |

**Rationale**: Each data type (relational metadata, vector embeddings, graph relationships) has fundamentally different access patterns. Specialized databases provide 10-100x better performance than forcing all data into a single system.

### 3. Async-First Backend

**Decision**: Build the entire backend with async Python (asyncio, asyncpg, ASGI).

**Rationale**: Document processing and LLM calls are I/O-bound operations. Async processing allows the backend to handle hundreds of concurrent requests without thread pooling overhead.

### 4. Clean Architecture Layers

**Decision**: Strict layered architecture with dependency inversion.

**Rationale**: The AI/ML landscape evolves rapidly. By isolating infrastructure (ChromaDB, Neo4j, OpenAI) behind abstract interfaces, we can swap implementations without touching business logic. For example, replacing ChromaDB with Pinecone or OpenAI with a local LLM.

---

## Data Flow Diagrams

### Document Processing (Write Path)

```
User uploads PDF
       │
       ▼
  API Endpoint validates (size, type)
       │
       ▼
  File saved to storage (local/S3)
       │
       ▼
  Document record created in PostgreSQL (status: "processing")
       │
       ▼
  Celery task dispatched (async)
       │
       ├──▶ Text extraction (PyMuPDF / Tesseract)
       ├──▶ Semantic chunking (512 tokens, 50 overlap)
       ├──▶ Embedding generation (Sentence Transformers)
       │         └──▶ Stored in ChromaDB
       ├──▶ NER entity extraction
       │         └──▶ Stored in Neo4j
       └──▶ Document record updated (status: "completed")
```

### Query Processing (Read Path)

```
User asks: "What is the maintenance schedule for P-101?"
       │
       ▼
  Query → Embedding (same model as indexing)
       │
       ▼
  ChromaDB similarity search (cosine, top-10)
       │
       ▼
  Retrieved chunks ranked by relevance
       │
       ▼
  Context assembled with source attribution
       │
       ▼
  LLM generates response (GPT-4o)
       │
       ▼
  Response + citations + confidence + suggestions
```

---

## Scalability Considerations

### Horizontal Scaling

| Component | Strategy |
|-----------|----------|
| Frontend | CDN + multiple Next.js instances |
| Backend | Multiple FastAPI workers behind load balancer |
| Workers | Additional Celery workers for document processing |
| PostgreSQL | Read replicas for query scaling |
| ChromaDB | Distributed mode or migrate to managed vector DB |
| Redis | Redis Cluster for cache scaling |

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| API response time (p50) | < 200ms | ~150ms (demo) |
| API response time (p99) | < 2s | ~1.5s (demo) |
| RAG query time | < 5s | ~3s (with LLM) |
| Document processing | < 60s/document | ~30s |
| Concurrent users | 100+ | Demo mode only |
| Document corpus | 10,000+ documents | Demo data |

---

## Caching Strategy

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Browser  │────▶│  Redis   │────▶│PostgreSQL│
│  Cache    │     │  Cache   │     │  (Source) │
│ (headers) │     │ (L2)     │     │          │
└──────────┘     └──────────┘     └──────────┘
```

| Cache Layer | TTL | Content |
|-------------|-----|---------|
| Browser | 5 min | Static assets, API responses |
| Redis L2 | 15 min | Dashboard aggregates, compliance scores |
| PostgreSQL | — | Source of truth |

---

## Failure Handling

| Failure Scenario | Handling Strategy |
|-----------------|-------------------|
| LLM API down | Fall back to demo responses |
| ChromaDB unreachable | Return error with cached results |
| Neo4j unreachable | Graph features degraded, core RAG works |
| Redis down | Bypass cache, hit database directly |
| File upload fails | Retry with exponential backoff (Tenacity) |
| Document processing fails | Mark as "failed", log error, notify user |

---

## Related Documentation

- [Architecture](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [AI Pipeline](AI_PIPELINE.md)
- [Database Design](DATABASE.md)
