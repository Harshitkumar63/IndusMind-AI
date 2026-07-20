"""
IndusMind AI — API Dependencies

Shared FastAPI dependencies for injection.
"""

from __future__ import annotations

from typing import Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_payload
from app.infrastructure.database import get_db


async def get_current_user(
    payload: dict[str, Any] = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Get the current authenticated user.
    In demo mode, returns a simulated user payload.
    In production, would look up the user from the database.
    """
    return payload


# Re-export for convenience
__all__ = ["get_db", "get_current_user"]
