"""
IndusMind AI — Named Entity Recognition

Extracts industrial entities (equipment, people, locations, etc.) from text
for knowledge graph construction.
"""

from __future__ import annotations

import re
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

# ─── Industrial Entity Patterns ────────────────────────────────

EQUIPMENT_PATTERNS = [
    r"\b([A-Z]{1,3}-\d{2,4}[A-Z]?)\b",  # P-101, C-201, E-301A
    r"\b(Pump|Compressor|Heat Exchanger|Boiler|Vessel|Motor|Valve|Turbine|Conveyor|Transformer)\s+([A-Z0-9\-]+)\b",
    r"\b(SV|CV|TV|PV|FV|LV)-\d{3,4}[A-Z]?\b",  # Safety valves, control valves
]

SOP_PATTERNS = [
    r"\bSOP[-\s]?[A-Z]?[-\s]?\d{3,4}\b",
    r"\bWork Instruction\s+[A-Z0-9\-]+\b",
    r"\bProcedure\s+[A-Z0-9\-]+\b",
]

REGULATION_PATTERNS = [
    r"\bOSHA\s+\d+\s+CFR\s+\d+\.\d+(?:\([a-z]\))?",
    r"\bISO\s+\d{4,5}(?:[-:]\d{4})?\s*(?:Section\s+\d+(?:\.\d+)?)?",
    r"\bAPI\s+\d{3,4}(?:\s+Section\s+\d+)?",
    r"\bASME\s+[A-Z]+\s*\d*",
    r"\bNFPA\s+\d{2,4}",
]

INCIDENT_PATTERNS = [
    r"\bINC[-\s]?\d{4}[-\s]?\d{2,4}\b",
    r"\bIncident\s+#?\d+\b",
    r"\bNCR[-\s]?\d{4,6}\b",  # Non-conformance reports
]

LOCATION_PATTERNS = [
    r"\bUnit[-\s]?\d+\s*(?:[A-Za-z\s]+)?",
    r"\bArea[-\s]?\d+\b",
    r"\bPlant\s+\d+\b",
    r"\bBlock[-\s]?[A-Z]\d*\b",
]

PERSON_PATTERNS = [
    r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.|Eng\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b",
    r"\bApproved by:\s*([A-Za-z\s]+)\b",
    r"\bInspected by:\s*([A-Za-z\s]+)\b",
    r"\bReported by:\s*([A-Za-z\s]+)\b",
]


class EntityExtractor:
    """
    Rule-based and NLP entity extraction for industrial documents.

    Extracts: Equipment, SOPs, Regulations, Incidents, Locations, People
    """

    def extract_entities(self, text: str) -> dict[str, list[dict[str, Any]]]:
        """
        Extract all entity types from text.

        Returns dict of entity_type -> list of {name, type, positions, confidence}
        """
        entities: dict[str, list[dict[str, Any]]] = {
            "equipment": [],
            "sop": [],
            "regulation": [],
            "incident": [],
            "location": [],
            "person": [],
        }

        # Equipment
        for pattern in EQUIPMENT_PATTERNS:
            for match in re.finditer(pattern, text):
                name = match.group(0).strip()
                if name and name not in [e["name"] for e in entities["equipment"]]:
                    entities["equipment"].append({
                        "name": name,
                        "type": "equipment",
                        "position": match.start(),
                        "confidence": 0.9,
                    })

        # SOPs
        for pattern in SOP_PATTERNS:
            for match in re.finditer(pattern, text):
                name = match.group(0).strip()
                if name and name not in [e["name"] for e in entities["sop"]]:
                    entities["sop"].append({
                        "name": name,
                        "type": "sop",
                        "position": match.start(),
                        "confidence": 0.85,
                    })

        # Regulations
        for pattern in REGULATION_PATTERNS:
            for match in re.finditer(pattern, text):
                name = match.group(0).strip()
                if name and name not in [e["name"] for e in entities["regulation"]]:
                    entities["regulation"].append({
                        "name": name,
                        "type": "regulation",
                        "position": match.start(),
                        "confidence": 0.92,
                    })

        # Incidents
        for pattern in INCIDENT_PATTERNS:
            for match in re.finditer(pattern, text):
                name = match.group(0).strip()
                if name and name not in [e["name"] for e in entities["incident"]]:
                    entities["incident"].append({
                        "name": name,
                        "type": "incident",
                        "position": match.start(),
                        "confidence": 0.88,
                    })

        # Locations
        for pattern in LOCATION_PATTERNS:
            for match in re.finditer(pattern, text):
                name = match.group(0).strip()
                if len(name) > 3 and name not in [e["name"] for e in entities["location"]]:
                    entities["location"].append({
                        "name": name,
                        "type": "location",
                        "position": match.start(),
                        "confidence": 0.8,
                    })

        # People
        for pattern in PERSON_PATTERNS:
            for match in re.finditer(pattern, text):
                name = match.group(0).strip()
                # Clean prefixes
                for prefix in ["Approved by:", "Inspected by:", "Reported by:"]:
                    name = name.replace(prefix, "").strip()
                if name and len(name) > 3 and name not in [e["name"] for e in entities["person"]]:
                    entities["person"].append({
                        "name": name,
                        "type": "person",
                        "position": match.start(),
                        "confidence": 0.75,
                    })

        total = sum(len(v) for v in entities.values())
        logger.info(f"Extracted {total} entities from text", breakdown={k: len(v) for k, v in entities.items()})
        return entities

    def extract_relationships(
        self,
        entities: dict[str, list[dict[str, Any]]],
        text: str,
    ) -> list[dict[str, Any]]:
        """
        Infer relationships between extracted entities based on co-occurrence
        and contextual patterns.
        """
        relationships: list[dict[str, Any]] = []

        # Equipment → Location (co-occurrence in same paragraph)
        paragraphs = text.split("\n\n")
        for para in paragraphs:
            para_equipment = [e for e in entities.get("equipment", []) if e["name"] in para]
            para_locations = [e for e in entities.get("location", []) if e["name"] in para]
            para_people = [e for e in entities.get("person", []) if e["name"] in para]
            para_sops = [e for e in entities.get("sop", []) if e["name"] in para]
            para_regulations = [e for e in entities.get("regulation", []) if e["name"] in para]

            for eq in para_equipment:
                for loc in para_locations:
                    relationships.append({
                        "source": eq["name"],
                        "source_type": "equipment",
                        "target": loc["name"],
                        "target_type": "location",
                        "relationship": "located_in",
                        "confidence": 0.7,
                    })
                for person in para_people:
                    relationships.append({
                        "source": eq["name"],
                        "source_type": "equipment",
                        "target": person["name"],
                        "target_type": "person",
                        "relationship": "maintained_by",
                        "confidence": 0.65,
                    })
                for sop in para_sops:
                    relationships.append({
                        "source": eq["name"],
                        "source_type": "equipment",
                        "target": sop["name"],
                        "target_type": "sop",
                        "relationship": "governed_by",
                        "confidence": 0.75,
                    })
                for reg in para_regulations:
                    relationships.append({
                        "source": eq["name"],
                        "source_type": "equipment",
                        "target": reg["name"],
                        "target_type": "regulation",
                        "relationship": "governed_by",
                        "confidence": 0.8,
                    })

        logger.info(f"Inferred {len(relationships)} relationships")
        return relationships


# Singleton
entity_extractor = EntityExtractor()
