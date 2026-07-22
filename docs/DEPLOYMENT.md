# Deployment Guide

> Deploying IndusMind AI to development, staging, and production environments

---

## Quick Start (Development)

### Frontend Only (Fastest)

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

The frontend runs with demo data out of the box — no backend required.

### Full Stack (Docker Compose)

```bash
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
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

---

## Docker Compose Architecture

```yaml
Services:
  frontend    → Next.js (port 3000)
  backend     → FastAPI (port 8000)
  postgres    → PostgreSQL 16 (port 5432)
  redis       → Redis 7 (port 6379)
  chromadb    → ChromaDB (port 8001)
  neo4j       → Neo4j 5 (port 7474/7687)
```

### Service Dependencies

```
frontend ──▶ backend ──▶ postgres (health check)
                     ──▶ redis (health check)
                     ──▶ chromadb
                     ──▶ neo4j
```

---

## Environment Variables

### Application

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `APP_NAME` | `IndusMind AI` | No | Application name |
| `APP_VERSION` | `1.0.0` | No | Application version |
| `APP_ENV` | `development` | No | Environment (development/staging/production) |
| `DEBUG` | `true` | No | Enable debug mode |
| `SECRET_KEY` | `change-me-in-production` | **Yes (prod)** | JWT signing key |
| `DEMO_MODE` | `true` | No | Enable demo mode |

### Database

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | Yes | Async PostgreSQL URL |
| `DATABASE_SYNC_URL` | `postgresql://...` | Yes | Sync PostgreSQL URL |

### Cache & Queue

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Yes | Redis connection URL |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Yes | Celery broker URL |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/2` | Yes | Celery results URL |

### AI Services

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `OPENAI_API_KEY` | — | **Yes (prod)** | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | No | LLM model |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | No | Local embedding model |
| `CHROMA_HOST` | `localhost` | Yes | ChromaDB host |
| `CHROMA_PORT` | `8000` | Yes | ChromaDB port |

### Knowledge Graph

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `NEO4J_URI` | `bolt://localhost:7687` | Yes | Neo4j connection |
| `NEO4J_USER` | `neo4j` | Yes | Neo4j username |
| `NEO4J_PASSWORD` | — | Yes | Neo4j password |

### File Storage

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `UPLOAD_DIR` | `./uploads` | No | Local upload directory |
| `MAX_UPLOAD_SIZE_MB` | `50` | No | Max file size (MB) |

---

## Production Deployment

### Pre-deployment Checklist

- [ ] Set `APP_ENV=production`
- [ ] Set `DEBUG=false`
- [ ] Set `DEMO_MODE=false`
- [ ] Generate a strong `SECRET_KEY` (e.g., `openssl rand -hex 32`)
- [ ] Set a valid `OPENAI_API_KEY`
- [ ] Use strong database passwords
- [ ] Configure CORS to your frontend domain only
- [ ] Enable HTTPS/TLS
- [ ] Set up database backups
- [ ] Configure log aggregation
- [ ] Set up monitoring and alerting

### Docker Production Build

```bash
# Build optimized images
docker compose -f docker/docker-compose.yml build --no-cache

# Run with production overrides
docker compose -f docker/docker-compose.yml up -d
```

### Cloud Deployment Options

#### AWS

```
ECS/Fargate  →  Application containers
RDS          →  PostgreSQL
ElastiCache  →  Redis
S3           →  File storage
CloudWatch   →  Monitoring
```

#### Google Cloud

```
Cloud Run    →  Application containers
Cloud SQL    →  PostgreSQL
Memorystore  →  Redis
Cloud Storage →  File storage
Cloud Logging →  Monitoring
```

#### Azure

```
Container Apps →  Application containers
Azure Database →  PostgreSQL
Azure Cache    →  Redis
Blob Storage   →  File storage
Azure Monitor  →  Monitoring
```

---

## Monitoring

### Health Check Endpoint

```
GET /health
```

Returns application status, version, and environment info.

### Key Metrics to Monitor

| Metric | Threshold | Action |
|--------|-----------|--------|
| API response time | > 2s | Scale backend |
| Error rate | > 1% | Check logs |
| Database connections | > 80% pool | Increase pool size |
| Redis memory | > 80% | Increase memory |
| ChromaDB query time | > 500ms | Optimize embeddings |
| Disk usage | > 80% | Clean uploads / expand |

---

## Related Documentation

- [Architecture](ARCHITECTURE.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [System Design](SYSTEM_DESIGN.md)
