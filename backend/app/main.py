"""
IndusMind AI — FastAPI Application Factory

Main application entry point with middleware, exception handlers, and API routing.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle."""
    setup_logging()
    logger.info(
        "Starting IndusMind AI",
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        demo_mode=settings.DEMO_MODE,
    )
    yield
    logger.info("Shutting down IndusMind AI")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "Industrial Knowledge Intelligence Platform — "
            "AI-powered document understanding, knowledge graph, "
            "maintenance intelligence, and compliance analysis "
            "for industrial operations."
        ),
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ─── CORS Middleware ───────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ─── Exception Handlers ───────────────────────────────
    register_exception_handlers(app)

    # ─── API Routes ────────────────────────────────────────
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # ─── Health Check ──────────────────────────────────────
    @app.get("/health", tags=["System"])
    async def health_check() -> dict:
        """Application health check endpoint."""
        return {
            **settings.get_app_metadata(),
            "status": "healthy",
        }

    @app.get("/", tags=["System"])
    async def root() -> dict:
        """Root endpoint — API information."""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "Industrial Knowledge Intelligence Platform",
            "docs": "/docs",
            "health": "/health",
            "api": f"{settings.API_V1_PREFIX}",
        }

    return app


# Application instance
app = create_app()
