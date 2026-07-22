# Developer Guide

> Everything you need to contribute to IndusMind AI

---

## Prerequisites

| Tool | Version | Installation |
|------|---------|-------------|
| Node.js | 20+ | [nodejs.org](https://nodejs.org/) |
| Python | 3.11+ | [python.org](https://python.org/) |
| Docker | Latest | [docker.com](https://docker.com/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |

---

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Harshitkumar63/IndusMind-AI.git
cd IndusMind-AI
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 3. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt
pip install -e ".[dev]"      # Development dependencies
cp .env.example .env
uvicorn app.main:app --reload --port 8000
# → http://localhost:8000
```

### 4. Full Stack (Docker)

```bash
cd docker
docker compose up -d
```

---

## Project Conventions

### File Naming

| Language | Convention | Example |
|----------|-----------|---------|
| Python | `snake_case.py` | `document_service.py` |
| TypeScript | `camelCase.ts` or `page.tsx` | `api.ts`, `page.tsx` |
| Components | `PascalCase.tsx` | (in `components/` when extracted) |
| Tests | `test_*.py` or `*.test.ts` | `test_health.py` |

### Code Organization

**Backend** — Follow Clean Architecture layers:
- `api/` — Route definitions only (thin controllers)
- `services/` — Business logic (orchestration)
- `domain/` — Models and enums (no dependencies)
- `infrastructure/` — External system adapters
- `ai/` — AI/ML pipeline modules
- `core/` — Cross-cutting concerns

**Frontend** — Follow Next.js App Router patterns:
- `app/` — Pages and layouts
- `lib/` — Utilities and API client
- `components/` — Shared components (future)

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(chat): add streaming response support
fix(documents): resolve PDF upload timeout
docs(api): add authentication flow documentation
refactor(backend): extract vector search service
test(rag): add integration tests for pipeline
```

---

## Adding a New API Endpoint

### 1. Create the domain model (if needed)

```python
# backend/app/domain/models/new_model.py
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base

class NewModel(Base):
    __tablename__ = "new_models"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
```

### 2. Create the service

```python
# backend/app/services/new_service.py
from app.core.logging import get_logger

logger = get_logger(__name__)

class NewService:
    async def get_items(self) -> list[dict]:
        logger.info("Fetching items")
        return [...]
```

### 3. Create the endpoint

```python
# backend/app/api/v1/endpoints/new_endpoint.py
from fastapi import APIRouter

router = APIRouter(prefix="/new", tags=["New"])

@router.get("")
async def list_items():
    return {"items": [...]}
```

### 4. Register the route

```python
# backend/app/api/v1/router.py
from app.api.v1.endpoints.new_endpoint import router as new_router
api_router.include_router(new_router)
```

---

## Adding a New Frontend Page

### 1. Create the page file

```tsx
// frontend/src/app/(platform)/new-page/page.tsx
"use client";

import { motion } from "framer-motion";

export default function NewPage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      <div>
        <h1 className="text-2xl font-bold">New Page</h1>
        <p className="text-[var(--muted-foreground)] text-sm mt-1">
          Description of the new page
        </p>
      </div>
      {/* Page content */}
    </div>
  );
}
```

### 2. Add to sidebar navigation

```typescript
// frontend/src/app/(platform)/layout.tsx — navItems array
{ href: "/new-page", icon: IconName, label: "New Page", badge: null },
```

---

## Running Tests

### Backend

```bash
cd backend
python -m pytest tests/ -v              # Run all tests
python -m pytest tests/ -v --tb=short   # Short tracebacks
python -m pytest tests/ --cov=app       # With coverage
```

### Frontend

```bash
cd frontend
npm run lint          # ESLint
npx tsc --noEmit      # Type check
npm run build         # Build check
```

---

## Useful Commands

```bash
# Format backend code
cd backend && ruff format .

# Lint backend code
cd backend && ruff check . --fix

# Format frontend code
cd frontend && npx prettier --write .

# Reset Docker volumes
cd docker && docker compose down -v

# View backend logs
cd docker && docker compose logs -f backend

# Access PostgreSQL
docker exec -it docker-postgres-1 psql -U indusmind -d indusmind_db
```

---

## Related Documentation

- [Architecture](ARCHITECTURE.md)
- [API Reference](API.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Deployment Guide](DEPLOYMENT.md)
