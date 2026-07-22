"""
IndusMind AI — Pydantic Schemas

Request/response DTOs for all API endpoints.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ─── Base Schemas ──────────────────────────────────────────────


class IndusMindBase(BaseModel):
    """Base schema with ORM mode enabled."""

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    """Standard paginated response wrapper."""

    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class StatusResponse(BaseModel):
    """Simple status response."""

    status: str
    message: str


# ─── User Schemas ──────────────────────────────────────────────


class UserResponse(IndusMindBase):
    id: uuid.UUID
    clerk_id: str
    email: str
    full_name: str
    role: str
    department: str | None = None
    avatar_url: str | None = None
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    department: str | None = None
    avatar_url: str | None = None
    preferences: dict | None = None


# ─── Document Schemas ──────────────────────────────────────────


class DocumentUploadResponse(IndusMindBase):
    id: uuid.UUID
    title: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    uploaded_at: datetime


class DocumentResponse(IndusMindBase):
    id: uuid.UUID
    title: str
    original_filename: str
    file_type: str
    file_size: int
    category: str
    tags: list[str] | None = None
    status: str
    processing_progress: float
    chunk_count: int
    uploaded_at: datetime
    processed_at: datetime | None = None


class DocumentDetailResponse(DocumentResponse):
    extracted_text: str | None = None
    metadata_json: dict | None = None
    user_id: uuid.UUID


class DocumentUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    tags: list[str] | None = None


class ChunkResponse(IndusMindBase):
    id: uuid.UUID
    chunk_index: int
    content: str
    token_count: int
    embedding_id: str | None = None


# ─── Chat Schemas ──────────────────────────────────────────────


class ConversationCreate(BaseModel):
    title: str | None = "New Conversation"
    context_type: str | None = None
    context_id: uuid.UUID | None = None


class ConversationResponse(IndusMindBase):
    id: uuid.UUID
    title: str
    context_type: str | None = None
    message_count: int
    last_message_at: datetime | None = None
    created_at: datetime


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)


class CitationDetail(BaseModel):
    document_id: uuid.UUID
    document_title: str
    chunk_id: uuid.UUID
    chunk_content: str
    relevance_score: float


class MessageResponse(IndusMindBase):
    id: uuid.UUID
    role: str
    content: str
    citations: list[CitationDetail] | None = None
    confidence_score: float | None = None
    suggested_questions: list[str] | None = None
    created_at: datetime


class ConversationDetailResponse(ConversationResponse):
    messages: list[MessageResponse] = []


class ChatStreamChunk(BaseModel):
    """Schema for streaming chat response chunks."""

    type: str  # "token", "citation", "done", "error"
    content: str | None = None
    citation: CitationDetail | None = None
    confidence_score: float | None = None
    suggested_questions: list[str] | None = None


# ─── Equipment Schemas ──────────────────────────────────────────


class EquipmentCreate(BaseModel):
    equipment_id: str = Field(..., description="Plant tag e.g. P-101")
    name: str
    type: str
    department: str | None = None
    location: str | None = None
    criticality: str = "medium"
    status: str = "running"
    install_date: date | None = None
    specifications: dict | None = None
    description: str | None = None


class EquipmentResponse(IndusMindBase):
    id: uuid.UUID
    equipment_id: str
    name: str
    type: str
    department: str | None = None
    location: str | None = None
    criticality: str
    status: str
    install_date: date | None = None
    last_maintenance: date | None = None
    next_maintenance: date | None = None
    created_at: datetime


class EquipmentDetailResponse(EquipmentResponse):
    specifications: dict | None = None
    description: str | None = None
    incident_count: int = 0
    maintenance_count: int = 0


class EquipmentHealthResponse(BaseModel):
    equipment_id: str
    name: str
    health_score: float
    risk_level: str
    days_since_maintenance: int | None = None
    predicted_failure_days: int | None = None
    recommendations: list[str]


# ─── Maintenance Schemas ────────────────────────────────────────


class MaintenanceCreate(BaseModel):
    equipment_id: uuid.UUID | None = None
    work_order: str
    type: str
    priority: str = "medium"
    description: str | None = None
    scheduled_date: date | None = None


class MaintenanceResponse(IndusMindBase):
    id: uuid.UUID
    work_order: str
    type: str
    priority: str
    status: str
    description: str | None = None
    scheduled_date: date | None = None
    completed_date: date | None = None
    cost: float | None = None
    downtime_hours: float | None = None
    created_at: datetime


class MaintenanceIntelligenceResponse(BaseModel):
    total_records: int
    overdue_count: int
    avg_downtime_hours: float
    total_cost: float
    critical_equipment: list[EquipmentHealthResponse]
    failure_predictions: list[dict]
    recommendations: list[str]


# ─── Compliance Schemas ──────────────────────────────────────────


class ComplianceResponse(IndusMindBase):
    id: uuid.UUID
    regulation_ref: str | None = None
    standard: str
    category: str | None = None
    status: str
    score: float | None = None
    findings: list[str] | None = None
    violations: list[str] | None = None
    recommendations: list[str] | None = None
    audit_date: date | None = None
    next_audit_date: date | None = None
    created_at: datetime


class ComplianceScoreResponse(BaseModel):
    overall_score: float
    by_standard: dict[str, float]
    total_audits: int
    compliant_count: int
    non_compliant_count: int
    pending_count: int
    active_violations: int


class ComplianceAuditSummary(BaseModel):
    summary: str
    key_findings: list[str]
    critical_violations: list[str]
    recommendations: list[str]
    risk_areas: list[str]


# ─── Analytics Schemas ────────────────────────────────────────


class DashboardSummary(BaseModel):
    total_documents: int
    total_equipment: int
    total_incidents: int
    compliance_score: float
    maintenance_due: int
    active_users: int
    recent_uploads: list[DocumentResponse]


class IncidentTrend(BaseModel):
    month: str
    critical: int
    major: int
    minor: int
    observation: int


class EquipmentHealthRanking(BaseModel):
    equipment_id: str
    name: str
    health_score: float
    incident_count: int
    maintenance_count: int
    status: str


class AnalyticsTrend(BaseModel):
    label: str
    value: float


# ─── Search Schemas ───────────────────────────────────────────


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    filters: dict | None = None
    page: int = 1
    page_size: int = 20


class SearchResult(BaseModel):
    id: uuid.UUID
    type: str  # "document", "equipment", "conversation", "knowledge_node"
    title: str
    snippet: str
    relevance_score: float
    metadata: dict | None = None


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    query: str
    processing_time_ms: float
