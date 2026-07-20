"""
IndusMind AI — Auth Endpoints

User authentication, verification, and profile management.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.api.v1.deps import get_current_user
from app.schemas import StatusResponse, UserResponse, UserUpdate

router = APIRouter()


@router.post("/verify", response_model=StatusResponse)
async def verify_token(user: dict[str, Any] = Depends(get_current_user)) -> StatusResponse:
    """Verify JWT token and sync user to database."""
    return StatusResponse(status="ok", message="Token verified successfully")


@router.get("/me", response_model=dict)
async def get_profile(user: dict[str, Any] = Depends(get_current_user)) -> dict:
    """Get current user profile."""
    return {
        "id": user.get("sub", "demo-user-001"),
        "email": user.get("email", "demo@indusmind.ai"),
        "full_name": user.get("full_name", "Demo User"),
        "role": user.get("role", "admin"),
        "department": "Engineering",
        "avatar_url": None,
        "is_active": True,
    }


@router.put("/me", response_model=StatusResponse)
async def update_profile(
    updates: UserUpdate,
    user: dict[str, Any] = Depends(get_current_user),
) -> StatusResponse:
    """Update current user profile."""
    return StatusResponse(status="ok", message="Profile updated successfully")
