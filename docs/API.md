# API Reference

> Complete REST API documentation for IndusMind AI

---

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except health check) require a JWT token in demo mode or a valid Bearer token in production.

```
Authorization: Bearer <token>
```

> **Demo Mode**: When `DEMO_MODE=true`, authentication is bypassed with a simulated demo user context.

## Response Format

All responses follow this structure:

```json
{
  "data": { ... },
  "message": "Success",
  "status": 200
}
```

Error responses:

```json
{
  "detail": "Error description",
  "status": 400
}
```

---

## System

### Health Check

```
GET /health
```

Returns application health and metadata.

**Response** `200 OK`
```json
{
  "name": "IndusMind AI",
  "version": "1.0.0",
  "environment": "development",
  "demo_mode": true,
  "status": "healthy"
}
```

---

## Authentication

### Login

```
POST /api/v1/auth/login
```

**Request Body**
```json
{
  "email": "admin@indusmind.ai",
  "password": "demo123"
}
```

**Response** `200 OK`
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "admin@indusmind.ai",
    "full_name": "Demo User",
    "role": "admin"
  }
}
```

---

## Documents

### List Documents

```
GET /api/v1/documents
```

**Query Parameters**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `category` | string | — | Filter by category |
| `status` | string | — | Filter by processing status |
| `skip` | int | 0 | Pagination offset |
| `limit` | int | 20 | Page size (max 100) |

**Response** `200 OK`
```json
{
  "documents": [
    {
      "id": "uuid",
      "title": "P-101 Maintenance Manual",
      "file_type": "pdf",
      "category": "manual",
      "status": "completed",
      "page_count": 45,
      "chunk_count": 128,
      "file_size": 4523000,
      "created_at": "2025-06-15T09:30:00Z"
    }
  ],
  "total": 1247,
  "skip": 0,
  "limit": 20
}
```

### Upload Document

```
POST /api/v1/documents/upload
Content-Type: multipart/form-data
```

**Request Body**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | ✅ | PDF, DOCX, XLSX, CSV, or image |
| `title` | string | — | Custom title (defaults to filename) |
| `category` | string | — | Document category |

**Response** `201 Created`

### Get Document

```
GET /api/v1/documents/{document_id}
```

### Delete Document

```
DELETE /api/v1/documents/{document_id}
```

---

## AI Chat

### Create Conversation

```
POST /api/v1/chat/conversations
```

**Request Body**
```json
{
  "title": "Pump P-101 Maintenance Query"
}
```

### Send Message (RAG Query)

```
POST /api/v1/chat/conversations/{conversation_id}/messages
```

**Request Body**
```json
{
  "content": "What is the maintenance schedule for pump P-101?"
}
```

**Response** `200 OK`
```json
{
  "id": "uuid",
  "role": "assistant",
  "content": "Based on the maintenance manual...",
  "citations": [
    {
      "document_title": "P-101 Maintenance Manual",
      "chunk_content": "Section 4.2: Quarterly maintenance...",
      "relevance_score": 0.95
    }
  ],
  "confidence_score": 0.92,
  "suggested_questions": [
    "What is the bearing replacement interval?",
    "Show me vibration analysis results"
  ]
}
```

### List Conversations

```
GET /api/v1/chat/conversations
```

---

## Knowledge Graph

### Get Full Graph

```
GET /api/v1/knowledge-graph
```

**Response** `200 OK`
```json
{
  "nodes": [
    {
      "id": "uuid",
      "type": "Equipment",
      "name": "Pump P-101",
      "properties": { "location": "Unit-1", "health_score": 78.5 }
    }
  ],
  "edges": [
    {
      "source": "uuid-1",
      "target": "uuid-2",
      "relationship": "MAINTAINED_BY",
      "weight": 0.85
    }
  ]
}
```

### Search Nodes

```
GET /api/v1/knowledge-graph/search?q=pump
```

---

## Equipment

### List Equipment

```
GET /api/v1/equipment
```

### Get Equipment Details

```
GET /api/v1/equipment/{equipment_id}
```

---

## Maintenance

### List Maintenance Records

```
GET /api/v1/maintenance
```

### Get Maintenance Intelligence

```
GET /api/v1/maintenance/intelligence
```

Returns AI-generated maintenance insights including failure predictions, recommended actions, and cost analysis.

---

## Compliance

### List Compliance Records

```
GET /api/v1/compliance
```

### Get Overall Compliance Score

```
GET /api/v1/compliance/score
```

**Response** `200 OK`
```json
{
  "overall_score": 81.6,
  "standards": [
    { "standard": "API 510", "score": 95, "status": "compliant" },
    { "standard": "ISO 45001", "score": 88, "status": "compliant" },
    { "standard": "OSHA PSM", "score": 85, "status": "compliant" },
    { "standard": "ISO 14001", "score": 55, "status": "non_compliant" }
  ],
  "total_violations": 7,
  "critical_violations": 2
}
```

---

## Analytics

### Dashboard Aggregates

```
GET /api/v1/analytics/dashboard
```

Returns all dashboard KPI data in a single optimized response.

---

## Search

### Full-Text Search

```
GET /api/v1/search?q=vibration+analysis
```

### Semantic Search

```
GET /api/v1/search/semantic?q=how+to+maintain+centrifugal+pumps
```

Uses vector similarity search across embedded document chunks.

---

## Error Codes

| Code | Description |
|------|-------------|
| `400` | Bad Request — Invalid input |
| `401` | Unauthorized — Missing or invalid token |
| `403` | Forbidden — Insufficient permissions |
| `404` | Not Found — Resource doesn't exist |
| `413` | Payload Too Large — File exceeds size limit |
| `422` | Unprocessable Entity — Validation error |
| `500` | Internal Server Error |
| `503` | Service Unavailable — External service down |

---

## Interactive Documentation

FastAPI provides auto-generated interactive docs:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## Related Documentation

- [Architecture](ARCHITECTURE.md)
- [AI Pipeline](AI_PIPELINE.md)
- [Database Design](DATABASE.md)
