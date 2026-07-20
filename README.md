<div align="center">

# 🧠 IndusMind AI

### Industrial Knowledge Intelligence Platform

**"The AI Brain for Industrial Operations"**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript)](https://typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)](https://docker.com/)

<br/>

Transform thousands of PDFs, SOPs, inspection reports, and maintenance logs into **structured, searchable intelligence**.

Ask questions. Get answers with citations. Predict failures. Ensure compliance.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Screenshots](#-screenshots)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [AI Pipeline](#-ai-pipeline)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## 🌟 Overview

**IndusMind AI** is an enterprise-grade AI platform that solves the **unstructured knowledge problem** in industrial organizations. Plants generate thousands of documents—maintenance manuals, inspection reports, SOPs, compliance records—but this knowledge is trapped in PDFs and spreadsheets. Engineers waste hours searching for answers.

IndusMind AI transforms this chaos into an intelligent, queryable knowledge base using:
- **RAG (Retrieval-Augmented Generation)** for precise Q&A with source citations
- **Knowledge Graphs** to map relationships between equipment, people, regulations, and processes
- **Predictive Maintenance** intelligence from historical failure data
- **Compliance Analysis** against OSHA, ISO, and API standards

### Target Users
| Role | Use Case |
|------|----------|
| Plant Engineers | Equipment troubleshooting, technical queries |
| Maintenance Engineers | Predictive maintenance, work order intelligence |
| Safety Officers | Incident analysis, safety compliance checks |
| Quality Engineers | Audit preparation, gap analysis |
| Operations Managers | Dashboard oversight, KPI monitoring |

---

## ✨ Features

### 🔍 AI-Powered RAG Chat
- Natural language Q&A over your entire document corpus
- Source citations with relevance scores
- Conversation history and context threading
- Suggested follow-up questions
- Confidence scoring

### 📄 Document Intelligence
- Drag-and-drop upload (PDF, DOCX, XLSX, CSV, Images)
- OCR for scanned documents (Tesseract/PyMuPDF)
- Automatic text extraction and semantic chunking
- Embedding generation and vector storage (ChromaDB)
- Grid/list view with category filtering

### 🕸️ Knowledge Graph
- Automatic entity extraction (Equipment, People, SOPs, Regulations)
- Relationship inference via co-occurrence analysis
- Interactive visualization (React Flow with custom nodes)
- Neo4j-backed graph storage
- Entity type filtering and search

### 🔧 Maintenance Intelligence
- Equipment health scoring and risk assessment
- Failure prediction with probability estimates
- Work order tracking (preventive, corrective, predictive, breakdown)
- AI-generated maintenance recommendations
- Cost tracking and trend analysis

### 🛡️ Compliance Analysis
- Multi-standard compliance scoring (OSHA, ISO, API, ASME)
- Violation tracking with severity and assignment
- AI-powered audit summaries
- Trend analysis over time
- Gap identification with recommendations

### 📊 Analytics Dashboard
- 6 KPI summary cards with trend indicators
- Incident severity distribution (stacked area chart)
- Equipment health comparison (horizontal bar chart)
- Compliance trend (line chart)
- Document category distribution (donut chart)
- Knowledge coverage assessment (animated circles)
- Maintenance cost tracking (area chart)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       PRESENTATION LAYER                      │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐ │
│  │  Landing Page │  │  Platform   │  │   Platform Pages     │ │
│  │  (Next.js)   │  │  Layout +   │  │ Dashboard, Chat, KG, │ │
│  │              │  │  Sidebar    │  │ Docs, Maintenance,   │ │
│  │              │  │             │  │ Compliance, Analytics │ │
│  └──────────────┘  └────────────┘  └──────────────────────┘ │
│         Next.js 15 • React • TypeScript • Tailwind CSS        │
└───────────────────────────┬──────────────────────────────────┘
                            │ REST API (Axios)
┌───────────────────────────┼──────────────────────────────────┐
│                       API GATEWAY                             │
│  ┌────────────────────────┴───────────────────────────────┐  │
│  │              FastAPI (Uvicorn ASGI)                     │  │
│  │  /auth  /documents  /chat  /knowledge-graph            │  │
│  │  /equipment  /maintenance  /compliance  /analytics     │  │
│  └────────────────────────┬───────────────────────────────┘  │
│         CORS • JWT Auth • RBAC • Demo Mode Bypass             │
└───────────────────────────┼──────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                       SERVICE LAYER                           │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Document    │  │  Chat/RAG    │  │  Knowledge Graph   │  │
│  │  Service     │  │  Service     │  │  Service           │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Analytics   │  │  Maintenance │  │  Compliance        │  │
│  │  Service     │  │  Service     │  │  Service           │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└───────────────────────────┼──────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                       AI PIPELINE                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  OCR/Text    │  │  Embeddings  │  │  RAG Pipeline      │  │
│  │  Extraction  │  │  Generator   │  │  (Query→Retrieve   │  │
│  │  (PyMuPDF,   │  │  (Sentence   │  │   →Generate→Cite)  │  │
│  │   Tesseract) │  │  Transformers│  │                    │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  NER Entity  │  │  Text        │  │  LLM Gateway       │  │
│  │  Extraction  │  │  Chunker     │  │  (OpenAI/Local)    │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└───────────────────────────┼──────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │PostgreSQL│  │ChromaDB  │  │  Neo4j   │  │    Redis     │ │
│  │(Metadata)│  │(Vectors) │  │ (Graph)  │  │  (Cache)     │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘ │
│  ┌──────────────────────┐  ┌──────────────────────────────┐  │
│  │  File Storage        │  │  Celery Workers              │  │
│  │  (Local/S3)          │  │  (Async Document Processing) │  │
│  └──────────────────────┘  └──────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| **Next.js 15** | React framework with App Router |
| **TypeScript** | Type-safe development |
| **Tailwind CSS** | Utility-first styling |
| **Framer Motion** | Animations & transitions |
| **Recharts** | Data visualization (charts) |
| **React Flow** | Knowledge graph visualization |
| **Lucide Icons** | Icon library |
| **Radix UI** | Accessible primitives |
| **Axios** | HTTP client |
| **Zustand** | State management |

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | ASGI web framework |
| **Python 3.11** | Core language |
| **SQLAlchemy 2.0** | Async ORM (Mapped style) |
| **Pydantic v2** | Validation & settings |
| **Structlog** | Structured logging |
| **Celery** | Async task queue |

### AI / ML
| Technology | Purpose |
|-----------|---------|
| **OpenAI GPT-4o** | LLM for RAG responses |
| **Sentence Transformers** | Local embedding generation |
| **ChromaDB** | Vector similarity search |
| **Neo4j** | Knowledge graph storage |
| **PyMuPDF** | PDF text extraction |
| **Tesseract OCR** | Scanned document OCR |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| **PostgreSQL 16** | Primary database |
| **Redis 7** | Caching & task broker |
| **Docker Compose** | Container orchestration |

---

## 📁 Project Structure

```
IndusMind AI/
├── frontend/                 # Next.js 15 Application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx                    # Landing page
│   │   │   ├── layout.tsx                  # Root layout
│   │   │   ├── globals.css                 # Design system
│   │   │   └── (platform)/                 # Platform route group
│   │   │       ├── layout.tsx              # Sidebar + Top bar
│   │   │       ├── dashboard/page.tsx      # Analytics dashboard
│   │   │       ├── chat/page.tsx           # AI RAG chat
│   │   │       ├── documents/page.tsx      # Document management
│   │   │       ├── knowledge-graph/page.tsx# Interactive graph
│   │   │       ├── maintenance/page.tsx    # Maintenance intelligence
│   │   │       ├── compliance/page.tsx     # Compliance analysis
│   │   │       ├── analytics/page.tsx      # Detailed analytics
│   │   │       └── settings/page.tsx       # Platform settings
│   │   └── lib/
│   │       ├── api.ts                      # Axios API client
│   │       └── utils.ts                    # Utility functions
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── main.py                         # Application factory
│   │   ├── seed.py                         # Demo data generator
│   │   ├── core/
│   │   │   ├── config.py                   # Pydantic settings
│   │   │   ├── security.py                 # JWT + RBAC + demo mode
│   │   │   ├── logging.py                  # Structlog config
│   │   │   └── exceptions.py               # Domain exceptions
│   │   ├── domain/models/                  # SQLAlchemy ORM models
│   │   │   ├── user.py, document.py, chunk.py
│   │   │   ├── equipment.py, incident.py
│   │   │   ├── maintenance.py, compliance.py
│   │   │   ├── conversation.py, message.py
│   │   │   └── knowledge.py
│   │   ├── schemas/                        # Pydantic DTOs
│   │   │   └── __init__.py                 # All request/response models
│   │   ├── api/v1/
│   │   │   ├── router.py                   # Route aggregator
│   │   │   └── endpoints/                  # 9 API modules
│   │   │       ├── auth.py, documents.py, chat.py
│   │   │       ├── knowledge_graph.py, equipment.py
│   │   │       ├── maintenance.py, compliance.py
│   │   │       ├── analytics.py, search.py
│   │   ├── services/                       # Business logic
│   │   │   ├── document_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── knowledge_graph_service.py
│   │   │   └── analytics_service.py
│   │   ├── infrastructure/                 # External systems
│   │   │   ├── database.py                 # SQLAlchemy async engine
│   │   │   ├── redis.py                    # Redis cache client
│   │   │   ├── vector_store.py             # ChromaDB client
│   │   │   ├── graph_db.py                 # Neo4j driver
│   │   │   ├── storage.py                  # File storage
│   │   │   └── llm.py                      # LLM gateway (OpenAI)
│   │   ├── ai/                             # AI Pipeline
│   │   │   ├── ocr/extractor.py            # Multi-format extraction
│   │   │   ├── embeddings/generator.py     # Chunking + embeddings
│   │   │   ├── rag/pipeline.py             # Full RAG pipeline
│   │   │   └── ner/entity_extractor.py     # Industrial NER
│   │   └── workers/
│   │       └── tasks.py                    # Celery background tasks
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── .env / .env.example
│
├── docker/
│   ├── docker-compose.yml    # Full stack orchestration
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── database/
│   └── init.sql              # PostgreSQL initialization
│
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js 20+** and **npm**
- **Python 3.11+**
- **Docker & Docker Compose** (optional, for full stack)

### Quick Start (Frontend Only)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/indusmind-ai.git
cd indusmind-ai

# 2. Install frontend dependencies
cd frontend
npm install

# 3. Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) — the platform runs with demo data out of the box.

### Full Stack (Docker)

```bash
# Start all services
cd docker
docker compose up -d

# Services:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
# Neo4j:     http://localhost:7474
# ChromaDB:  http://localhost:8001
```

### Backend Only

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Start server
uvicorn app.main:app --reload --port 8000
```

---

## 🖼️ Screenshots

### Landing Page
Premium dark-mode landing with animated hero, feature cards, and stats bar.

### Dashboard
6 KPI cards, incident trends, equipment health, compliance score, document categories, recent uploads.

### AI Chat
ChatGPT-style interface with citations, confidence scores, suggested questions, and conversation history.

### Knowledge Graph
Interactive React Flow visualization with custom nodes colored by entity type, animated edges, and minimap.

### Maintenance Intelligence
Equipment health table with risk assessment, maintenance trend chart, AI recommendations.

### Compliance Analysis
Score gauge, standard-by-standard progress bars, violation tracker, AI audit summary.

---

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/auth/login` | User authentication |
| `GET` | `/documents` | List documents |
| `POST` | `/documents/upload` | Upload document |
| `GET` | `/documents/{id}` | Get document details |
| `POST` | `/chat/conversations` | Create conversation |
| `POST` | `/chat/conversations/{id}/messages` | Send message (RAG) |
| `GET` | `/knowledge-graph` | Get full graph |
| `GET` | `/knowledge-graph/search?q=` | Search nodes |
| `GET` | `/equipment` | List equipment |
| `GET` | `/maintenance` | List maintenance records |
| `GET` | `/maintenance/intelligence` | AI insights |
| `GET` | `/compliance` | List compliance records |
| `GET` | `/compliance/score` | Overall score |
| `GET` | `/analytics/dashboard` | Dashboard aggregates |
| `GET` | `/search?q=` | Full-text search |
| `GET` | `/search/semantic?q=` | Semantic search |

Interactive docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗄️ Database Schema (ER Diagram)

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│    User      │     │   Document   │     │     Chunk      │
├─────────────┤     ├──────────────┤     ├────────────────┤
│ id (PK)     │     │ id (PK)      │     │ id (PK)        │
│ email       │──1:M│ uploaded_by   │──1:M│ document_id    │
│ full_name   │     │ title         │     │ content        │
│ role        │     │ file_type     │     │ chunk_index    │
│ department  │     │ category      │     │ embedding_id   │
│ hashed_pw   │     │ status        │     │ token_count    │
└─────────────┘     │ page_count    │     └────────────────┘
                    │ chunk_count   │
                    └──────────────┘

┌──────────────┐     ┌──────────────┐     ┌────────────────┐
│  Equipment   │     │   Incident   │     │  Maintenance   │
├──────────────┤     ├──────────────┤     ├────────────────┤
│ id (PK)      │     │ id (PK)      │     │ id (PK)        │
│ tag          │──1:M│ equipment_id │──1:M│ equipment_id   │
│ name         │     │ title        │     │ title          │
│ type         │     │ severity     │     │ type           │
│ health_score │     │ status       │     │ priority       │
│ status       │     │ description  │     │ status         │
│ location     │     │ root_cause   │     │ cost           │
└──────────────┘     └──────────────┘     └────────────────┘

┌──────────────┐     ┌──────────────┐     ┌────────────────┐
│  Compliance  │     │ Conversation │     │    Message     │
├──────────────┤     ├──────────────┤     ├────────────────┤
│ id (PK)      │     │ id (PK)      │     │ id (PK)        │
│ regulation   │     │ user_id (FK) │──1:M│ conversation_id│
│ standard     │     │ title        │     │ role           │
│ score        │     │ created_at   │     │ content        │
│ status       │     └──────────────┘     │ citations      │
│ violations   │                          │ confidence     │
└──────────────┘                          └────────────────┘

┌────────────────────────────────────────────────────────────┐
│                    Knowledge Graph (Neo4j)                  │
│  ┌────────────┐    relationship     ┌────────────┐         │
│  │ KnowledgeNode├─────────────────►│ KnowledgeNode│        │
│  │ • type      │                   │ • type       │        │
│  │ • name      │  (maintained_by,  │ • name       │        │
│  │ • properties│   governed_by,    │ • properties │        │
│  └────────────┘   located_in, etc) └────────────┘         │
└────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Pipeline

```
Document Upload → Text Extraction → Semantic Chunking → Embedding Generation
                        ↓                                       ↓
                  Entity Extraction                      ChromaDB Storage
                        ↓                                       ↓
                  Knowledge Graph                         User Query
                  (Neo4j Storage)                              ↓
                                                     Query Embedding
                                                           ↓
                                                    Vector Similarity
                                                    Search (Top-K)
                                                           ↓
                                                    Context Assembly
                                                           ↓
                                                    LLM Generation
                                                    (GPT-4o / Local)
                                                           ↓
                                                    Response + Citations
```

### Pipeline Steps

1. **OCR / Text Extraction** — PyMuPDF for native PDFs, Tesseract for scanned, python-docx/openpyxl for Office formats
2. **Semantic Chunking** — Sentence-boundary splitting with configurable overlap (512 tokens, 50 overlap)
3. **Embedding Generation** — Sentence Transformers (`all-MiniLM-L6-v2`) or OpenAI embeddings
4. **Vector Storage** — ChromaDB with cosine similarity and metadata filtering
5. **NER** — Regex-based extraction of equipment IDs, SOPs, regulations, incidents, locations, people
6. **Knowledge Graph** — Co-occurrence based relationship inference, stored in Neo4j
7. **RAG Query** — Embed query → retrieve top-K → assemble context → LLM generate → cite sources

---

## 🚢 Deployment

### Docker Compose (Recommended)

```bash
cd docker
docker compose up -d --build
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEMO_MODE` | `true` | Enable demo mode (no API keys needed) |
| `OPENAI_API_KEY` | — | OpenAI API key for production RAG |
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection |
| `CHROMA_HOST` | `localhost` | ChromaDB host |

---

## 📄 License

This project was built for the **AI Hackathon 2025**.

---

<div align="center">

**Built with ❤️ by the IndusMind AI Team**

*Transforming Industrial Knowledge into Actionable Intelligence*

</div>
