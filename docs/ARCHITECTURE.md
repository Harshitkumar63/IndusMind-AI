# Architecture

> System architecture for IndusMind AI — Industrial Knowledge Intelligence Platform

---

## Overview

IndusMind AI follows a **Clean Architecture** pattern with clear separation of concerns across four distinct layers. Each layer has a well-defined responsibility and communicates only with its adjacent layers.

```mermaid
graph TD
    subgraph Presentation Layer
        UI[Next.js 15 Frontend<br/>React 19, Tailwind CSS]
    end

    subgraph Application Layer
        API[FastAPI Backend<br/>REST API, Auth, RBAC]
    end

    subgraph Domain & Service Layer
        DocSvc[Document Service]
        ChatSvc[Chat & RAG Service]
        GraphSvc[Knowledge Graph Service]
    end

    subgraph AI Pipeline
        AIPipe[AI Orchestrator<br/>OCR, Chunking, NER]
        LLM[LLM Gateway<br/>OpenAI GPT-4o]
    end

    subgraph Infrastructure
        PG[(PostgreSQL)]
        CH[(ChromaDB)]
        N4J[(Neo4j)]
        RED[(Redis)]
    end

    UI -->|REST / HTTP| API
    API --> DocSvc & ChatSvc & GraphSvc
    DocSvc --> AIPipe
    ChatSvc --> AIPipe
    ChatSvc --> LLM
    AIPipe --> PG & CH & N4J
    API --> RED
```

---

## Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Single Responsibility** | Each service class handles one domain (documents, chat, maintenance) |
| **Open/Closed** | Infrastructure adapters are swappable (e.g., local storage → S3) |
| **Dependency Inversion** | Services depend on abstractions, not concrete database implementations |
| **Repository Pattern** | Infrastructure layer wraps all external system access |
| **Gateway Pattern** | `LLMGateway` provides a unified interface to OpenAI with demo fallback |
| **Service Layer** | All business logic lives in `services/`, keeping API endpoints thin |
| **Feature Modules** | Frontend pages are self-contained feature modules |

---

## Backend Architecture

### Layer Breakdown

```
backend/app/
├── api/                  # API Layer — Route definitions only
│   └── v1/
│       ├── router.py     # Route aggregator
│       ├── deps.py       # Dependency injection
│       └── endpoints/    # 9 endpoint modules
│
├── services/             # Service Layer — Business logic
│   ├── document_service.py
│   ├── chat_service.py
│   ├── knowledge_graph_service.py
│   └── analytics_service.py
│
├── domain/               # Domain Layer — Models & enums
│   ├── models/           # SQLAlchemy ORM models
│   └── enums.py          # Domain enumerations
│
├── ai/                   # AI Pipeline — ML & NLP
│   ├── ocr/              # Text extraction
│   ├── embeddings/       # Vector generation
│   ├── rag/              # Retrieval-Augmented Generation
│   └── ner/              # Named Entity Recognition
│
├── infrastructure/       # Infrastructure — External systems
│   ├── database.py       # PostgreSQL (async SQLAlchemy)
│   ├── vector_store.py   # ChromaDB
│   ├── graph_db.py       # Neo4j
│   ├── redis.py          # Redis cache
│   ├── storage.py        # File storage (local/S3)
│   └── llm.py            # LLM Gateway (OpenAI)
│
├── core/                 # Core — Cross-cutting concerns
│   ├── config.py         # Pydantic settings
│   ├── security.py       # JWT + RBAC
│   ├── logging.py        # Structlog
│   └── exceptions.py     # Domain exceptions
│
└── workers/              # Workers — Async processing
    └── tasks.py          # Celery tasks
```

### Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Router as FastAPI Router
    participant Endpoint as API Endpoint
    participant Service as Service Layer
    participant Infra as Infrastructure/AI

    Client->>Router: HTTP Request
    Router->>Endpoint: Validates input (Pydantic)
    Endpoint->>Service: Extracts params, calls service
    Service->>Infra: Executes Business Logic
    Infra-->>Service: Returns Data
    Service-->>Endpoint: Maps to Domain Models
    Endpoint-->>Router: Serialized via Pydantic
    Router-->>Client: HTTP Response
```

---

## Frontend Architecture

### Next.js App Router Structure

```
frontend/src/
├── app/
│   ├── page.tsx                      # Landing page (marketing)
│   ├── layout.tsx                    # Root layout (fonts, metadata)
│   ├── globals.css                   # Design system tokens
│   └── (platform)/                   # Route group (shared layout)
│       ├── layout.tsx                # Sidebar + Top bar
│       ├── dashboard/page.tsx        # Analytics dashboard
│       ├── chat/page.tsx             # AI RAG chat
│       ├── documents/page.tsx        # Document management
│       ├── knowledge-graph/page.tsx  # Knowledge graph viz
│       ├── maintenance/page.tsx      # Maintenance intelligence
│       ├── compliance/page.tsx       # Compliance analysis
│       ├── analytics/page.tsx        # Detailed analytics
│       └── settings/page.tsx         # Platform settings
└── lib/
    ├── api.ts                        # Axios API client
    └── utils.ts                      # Utility functions
```

### Design System

The frontend uses a CSS custom properties-based design system defined in `globals.css`:

- **Theme**: Dark mode with glassmorphism effects
- **Colors**: Indigo-to-violet gradient palette
- **Typography**: System font stack with semibold headings
- **Components**: Glass cards, badges, gradient buttons, animated transitions
- **Animations**: Framer Motion for page transitions, scroll-reveal, hover effects

---

## Data Flow

### Document Ingestion Pipeline

```mermaid
flowchart TD
    User[User] -->|Uploads PDF| Storage[File Storage<br/>local/S3]
    Storage --> Celery[Celery Worker<br/>Async]
    
    Celery --> OCR[OCR & Text Extraction<br/>PyMuPDF/Tesseract]
    Celery --> Chunk[Semantic Chunking<br/>512 tokens]
    Celery --> Embed[Embedding Generation<br/>Sentence Transformers]
    Celery --> NER[NER Entity Extraction<br/>Regex-based]
    Celery --> Meta[Metadata Update]
    
    Embed --> Chroma[(ChromaDB<br/>Vector Storage)]
    NER --> Neo4j[(Neo4j<br/>Knowledge Graph)]
    Meta --> PG[(PostgreSQL<br/>Document Record)]
```

### RAG Query Pipeline

```mermaid
flowchart TD
    Query([User Question]) --> QEmbed[Query Embedding<br/>Sentence Transformers]
    QEmbed --> VSearch[Vector Similarity Search<br/>ChromaDB, top-K]
    VSearch --> Context[Context Assembly<br/>Source Documents]
    Context --> LLM[LLM Generation<br/>GPT-4o / Demo Fallback]
    LLM --> Response([Response + Citations + Confidence])
```

---

## Security Architecture

| Layer | Mechanism |
|-------|-----------|
| **Authentication** | JWT tokens with configurable expiry |
| **Authorization** | Role-based access control (RBAC) |
| **Input Validation** | Pydantic v2 for all API inputs |
| **SQL Injection** | SQLAlchemy ORM with parameterized queries |
| **File Upload** | Type validation, size limits, path sanitization |
| **CORS** | Configurable allowed origins |
| **Secrets** | Environment variables via Pydantic Settings |
| **Demo Mode** | Bypass auth for evaluation (disabled in production) |

---

## Infrastructure Topology

```mermaid
graph TD
    FE[Frontend<br/>Next.js :3000] --> BE[Backend<br/>FastAPI :8000]
    BE --> CW[Celery Worker]
    
    BE --> PG[(PostgreSQL<br/>:5432)]
    BE --> CH[(ChromaDB<br/>:8001)]
    BE --> N4J[(Neo4j<br/>:7474)]
    BE --> RED[(Redis<br/>:6379)]
    
    CW --> PG
    CW --> CH
    CW --> N4J
    CW --> RED
```

---

## Related Documentation

- [Database Design](DATABASE.md)
- [API Reference](API.md)
- [AI Pipeline](AI_PIPELINE.md)
- [System Design](SYSTEM_DESIGN.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
