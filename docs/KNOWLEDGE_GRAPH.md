# Knowledge Graph

> Entity extraction, relationship inference, and graph storage in IndusMind AI

---

## Overview

IndusMind AI automatically constructs a knowledge graph from industrial documents. This graph maps relationships between equipment, people, regulations, procedures, locations, and incidents — enabling relationship-aware queries and visual exploration.

---

## Graph Schema

### Node Types

| Type | Color | Properties | Examples |
|------|-------|-----------|----------|
| **Equipment** | 🔵 Blue | tag, name, type, location, health_score | P-101, C-201, B-401 |
| **Person** | 🟢 Green | name, role, department | John Smith, Jane Doe |
| **SOP** | 🟣 Purple | code, title, version | SOP-2025-001 |
| **Regulation** | 🟠 Orange | standard, section, title | OSHA 1910.119 |
| **Location** | 🟡 Yellow | name, area, building | Unit-1, Control Room |
| **Incident** | 🔴 Red | id, title, severity, date | INC-2025-042 |

### Relationship Types

| Relationship | From | To | Description |
|-------------|------|-----|-------------|
| `MAINTAINED_BY` | Equipment | Person | Equipment maintenance assignments |
| `GOVERNED_BY` | Equipment | Regulation | Applicable regulatory standards |
| `LOCATED_IN` | Equipment | Location | Physical location mapping |
| `REFERENCED_IN` | Equipment | SOP | Mentions in procedures |
| `INVOLVED_IN` | Person | Incident | Incident participation |
| `CAUSED_BY` | Incident | Equipment | Root cause equipment |
| `RELATED_TO` | Equipment | Equipment | Co-occurrence relationships |
| `SUPERSEDES` | SOP | SOP | Document version chain |
| `APPLIES_TO` | Regulation | Location | Location-specific regulations |

---

## Entity Extraction Pipeline

### Stage 1: Pattern-Based NER

```python
class IndustrialNERExtractor:
    PATTERNS = {
        "equipment": r"[A-Z]{1,3}-\d{2,4}[A-Z]?",
        "sop": r"SOP[-\s]?\d{4}[-\s]?\d{2,4}",
        "regulation": r"(OSHA|ISO|API|ASME)\s*\d+[\.\-]?\d*",
        "incident": r"INC[-\s]?\d{4}[-\s]?\d{2,4}",
        "location": r"Unit[-\s]?\d+|Building\s+[A-Z]|Area\s+\d+",
    }
```

### Stage 2: Co-occurrence Analysis

Entities appearing within the same document section (chunk) are connected:

1. Extract all entities from each chunk
2. Create edges between all entity pairs in the same chunk
3. Weight = number of co-occurrences across all chunks
4. Relationship type inferred from entity type pair

### Stage 3: Neo4j Storage

```cypher
-- Create equipment node
MERGE (e:Equipment {tag: $tag})
SET e.name = $name, e.type = $type, e.health_score = $health_score

-- Create relationship
MATCH (e:Equipment {tag: $equipment_tag})
MATCH (r:Regulation {standard: $standard})
MERGE (e)-[:GOVERNED_BY {weight: $weight}]->(r)
```

---

## Graph Queries

### Find Equipment Relationships

```cypher
MATCH (e:Equipment {tag: "P-101"})-[r]-(connected)
RETURN e, r, connected
```

### Find Compliance Gaps

```cypher
MATCH (e:Equipment)
WHERE NOT (e)-[:GOVERNED_BY]->(:Regulation)
RETURN e.tag, e.name
```

### Find Maintenance Network

```cypher
MATCH (p:Person)-[:MAINTAINED_BY]-(e:Equipment)-[:LOCATED_IN]-(l:Location)
RETURN p.name, e.tag, l.name
```

### Shortest Path Between Entities

```cypher
MATCH path = shortestPath(
  (a:Equipment {tag: "P-101"})-[*]-(b:Regulation {standard: "OSHA 1910.119"})
)
RETURN path
```

---

## Frontend Visualization

The knowledge graph is visualized using **React Flow** with custom nodes:

- **Custom node types**: Color-coded by entity type with icons
- **Interactive**: Drag, zoom, pan, and click for details
- **Minimap**: Overview navigation
- **Filtering**: Show/hide entity types
- **Search**: Find nodes by name or tag
- **Animated edges**: Show relationship direction and weight

---

## API Endpoints

### Get Full Graph

```
GET /api/v1/knowledge-graph
```

### Search Nodes

```
GET /api/v1/knowledge-graph/search?q=P-101
```

### Get Node Neighbors

```
GET /api/v1/knowledge-graph/{node_id}/neighbors
```

---

## Related Documentation

- [AI Pipeline](AI_PIPELINE.md)
- [Database Design](DATABASE.md)
- [Architecture](ARCHITECTURE.md)
