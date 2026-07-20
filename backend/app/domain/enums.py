"""
IndusMind AI — Domain Enums

Centralized enum definitions for all domain models.
"""

from __future__ import annotations

import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    ENGINEER = "engineer"
    AUDITOR = "auditor"
    VIEWER = "viewer"


class DocumentType(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    CSV = "csv"
    TXT = "txt"
    IMAGE = "image"


class DocumentCategory(str, enum.Enum):
    SOP = "sop"
    MANUAL = "manual"
    INSPECTION = "inspection"
    MAINTENANCE = "maintenance"
    AUDIT = "audit"
    REPORT = "report"
    REGULATION = "regulation"
    DRAWING = "drawing"
    OTHER = "other"


class DocumentStatus(str, enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class EquipmentType(str, enum.Enum):
    PUMP = "pump"
    VALVE = "valve"
    MOTOR = "motor"
    COMPRESSOR = "compressor"
    HEAT_EXCHANGER = "heat_exchanger"
    VESSEL = "vessel"
    TURBINE = "turbine"
    BOILER = "boiler"
    TRANSFORMER = "transformer"
    CONVEYOR = "conveyor"
    OTHER = "other"


class EquipmentCriticality(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EquipmentStatus(str, enum.Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    FAILED = "failed"


class IncidentSeverity(str, enum.Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    OBSERVATION = "observation"


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class MaintenanceType(str, enum.Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    BREAKDOWN = "breakdown"


class MaintenancePriority(str, enum.Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MaintenanceStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class ComplianceStandard(str, enum.Enum):
    ISO_9001 = "iso_9001"
    ISO_14001 = "iso_14001"
    ISO_45001 = "iso_45001"
    OSHA = "osha"
    API = "api"
    ASME = "asme"
    NFPA = "nfpa"
    CUSTOM = "custom"


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY = "partially"
    PENDING = "pending"


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class KnowledgeNodeType(str, enum.Enum):
    EQUIPMENT = "equipment"
    PERSON = "person"
    DEPARTMENT = "department"
    LOCATION = "location"
    PROCESS = "process"
    SOP = "sop"
    REGULATION = "regulation"
    INCIDENT = "incident"
    MATERIAL = "material"


class KnowledgeRelationship(str, enum.Enum):
    MAINTAINED_BY = "maintained_by"
    LOCATED_IN = "located_in"
    GOVERNED_BY = "governed_by"
    CAUSED_BY = "caused_by"
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    INSPECTED_BY = "inspected_by"
    USES = "uses"
    PRODUCES = "produces"
    DEPENDS_ON = "depends_on"
