# Database Design

> Data model and database architecture for IndusMind AI

---

## Overview

IndusMind AI uses a **polyglot persistence** strategy with three specialized databases:

| Database | Purpose | Technology |
|----------|---------|------------|
| **Relational** | User data, documents, equipment, compliance | PostgreSQL 16 |
| **Vector** | Document embeddings for similarity search | ChromaDB |
| **Graph** | Knowledge graph (entities + relationships) | Neo4j 5 |

---

## Entity-Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Document : "uploads"
    User ||--o{ Conversation : "creates"
    Conversation ||--o{ Message : "contains"
    Document ||--o{ Chunk : "split_into"
    Equipment ||--o{ Incident : "has"
    Equipment ||--o{ Maintenance : "requires"
    
    User {
        UUID id PK
        string email UK
        string full_name
        string role
        string hashed_password
        boolean is_active
        datetime created_at
    }
    
    Document {
        UUID id PK
        UUID user_id FK
        string title
        string file_type
        string category
        string status
        int file_size
        int chunk_count
        datetime created_at
    }
    
    Chunk {
        UUID id PK
        UUID document_id FK
        string content
        int chunk_index
        string embedding_id
        int token_count
        jsonb metadata
    }
    
    Conversation {
        UUID id PK
        UUID user_id FK
        string title
        datetime created_at
    }
    
    Message {
        UUID id PK
        UUID conversation_id FK
        string role
        text content
        jsonb citations
        float confidence_score
        datetime created_at
    }
    
    Equipment {
        UUID id PK
        string tag UK
        string name
        string type
        float health_score
        string status
        string location
    }
    
    Incident {
        UUID id PK
        UUID equipment_id FK
        string title
        string severity
        string status
        text description
        datetime occurred_at
    }
    
    Maintenance {
        UUID id PK
        UUID equipment_id FK
        string title
        string type
        string priority
        string status
        float cost
        datetime scheduled_date
    }
    
    Compliance {
        UUID id PK
        string regulation
        string standard
        string section
        float score
        string status
        jsonb violations
        datetime next_audit_date
    }
```

---

## Enumerations

### UserRole
```
admin | engineer | viewer | auditor
```

### DocumentStatus
```
pending | processing | completed | failed
```

### DocumentCategory
```
manual | sop | inspection | maintenance | regulation | audit | report | other
```

### EquipmentStatus
```
operational | degraded | offline | maintenance | decommissioned
```

### EquipmentType
```
pump | compressor | boiler | exchanger | tank | valve | motor | turbine | vessel
```

### IncidentSeverity
```
critical | major | minor | informational
```

### MaintenanceType
```
preventive | corrective | predictive | breakdown
```

### MaintenancePriority
```
critical | high | medium | low
```

### ComplianceStandard
```
osha_psm | iso_45001 | iso_14001 | api_510 | api_570 | asme
```

---

## Vector Store (ChromaDB)

### Collection: `indusmind_documents`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique chunk identifier |
| `embedding` | float[384] | Sentence Transformer embedding vector |
| `document` | string | Original chunk text content |
| `metadata` | object | Document metadata (see below) |

#### Metadata Schema
```json
{
  "document_id": "uuid",
  "document_title": "string",
  "chunk_index": "integer",
  "page_number": "integer",
  "category": "string",
  "file_type": "string"
}
```

---

## Graph Database (Neo4j)

### Node Types

| Label | Properties | Description |
|-------|-----------|-------------|
| `Equipment` | tag, name, type, location, health_score | Plant equipment |
| `Person` | name, role, department | People referenced in documents |
| `SOP` | code, title, version | Standard Operating Procedures |
| `Regulation` | standard, section, title | Regulatory standards |
| `Location` | name, area, building | Physical locations |
| `Incident` | id, title, severity, date | Safety incidents |

### Relationship Types

| Relationship | From → To | Description |
|-------------|-----------|-------------|
| `MAINTAINED_BY` | Equipment → Person | Maintenance assignments |
| `GOVERNED_BY` | Equipment → Regulation | Applicable regulations |
| `LOCATED_IN` | Equipment → Location | Physical location |
| `REFERENCED_IN` | Equipment → SOP | Mentions in procedures |
| `INVOLVED_IN` | Person → Incident | Incident participation |
| `RELATED_TO` | Equipment → Equipment | Co-occurrence relationship |

---

## Indexing Strategy

### PostgreSQL Indexes

| Table | Column(s) | Type | Rationale |
|-------|-----------|------|-----------|
| `users` | `email` | UNIQUE B-tree | Login lookups |
| `documents` | `uploaded_by` | B-tree | User's documents |
| `documents` | `category` | B-tree | Category filtering |
| `documents` | `status` | B-tree | Processing queue |
| `chunks` | `document_id` | B-tree | Document chunks |
| `equipment` | `tag` | UNIQUE B-tree | Equipment lookups |
| `incidents` | `equipment_id` | B-tree | Equipment incidents |
| `maintenance` | `equipment_id` | B-tree | Equipment maintenance |
| `conversations` | `user_id` | B-tree | User conversations |

---

## Related Documentation

- [Architecture](ARCHITECTURE.md)
- [API Reference](API.md)
- [Deployment Guide](DEPLOYMENT.md)
