"""
IndusMind AI — Custom Exceptions

Domain-specific exception classes and FastAPI exception handlers.
"""

from __future__ import annotations

from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse

# ─── Domain Exceptions ─────────────────────────────────────────


class IndusMindError(Exception):
    """Base exception for all IndusMind domain errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


IndusMindException = IndusMindError


class EntityNotFoundError(IndusMindError):
    """Raised when a requested entity does not exist."""

    pass


class DocumentProcessingError(IndusMindError):
    """Raised when document processing fails."""

    pass


class AIServiceError(IndusMindError):
    """Raised when an AI service call fails."""

    pass


class StorageError(IndusMindError):
    """Raised when file storage operations fail."""

    pass


class ValidationError(IndusMindError):
    """Raised when domain validation fails."""

    pass


class AuthenticationError(IndusMindError):
    """Raised when authentication fails."""

    pass


class AuthorizationError(IndusMindError):
    """Raised when the user lacks required permissions."""

    pass


# ─── Exception Handlers ────────────────────────────────────────


async def entity_not_found_handler(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "not_found",
            "message": exc.message,
            "details": exc.details,
        },
    )


async def document_processing_handler(request: Request, exc: DocumentProcessingError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "processing_error",
            "message": exc.message,
            "details": exc.details,
        },
    )


async def ai_service_handler(request: Request, exc: AIServiceError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "ai_service_error",
            "message": exc.message,
            "details": exc.details,
        },
    )


async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "validation_error",
            "message": exc.message,
            "details": exc.details,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
        },
    )


def register_exception_handlers(app: Any) -> None:
    """Register all custom exception handlers on the FastAPI app."""
    app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
    app.add_exception_handler(DocumentProcessingError, document_processing_handler)
    app.add_exception_handler(AIServiceError, ai_service_handler)
    app.add_exception_handler(ValidationError, validation_handler)
