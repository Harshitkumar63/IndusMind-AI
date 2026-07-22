"""
IndusMind AI — Core Security

JWT verification, password hashing, and role-based access control.
"""

from __future__ import annotations

import enum
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# ─── Password Hashing ─────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return pwd_context.verify(plain, hashed)


# ─── JWT ───────────────────────────────────────────────────────


def create_access_token(
    subject: str,
    role: str = "viewer",
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token."""
    expire = datetime.now(UTC) + (expires_delta or timedelta(hours=24))
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(UTC),
        "iss": settings.APP_NAME,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            issuer=settings.APP_NAME,
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# ─── Role-Based Access Control ─────────────────────────────────


class UserRole(str, enum.Enum):
    """Platform user roles with hierarchical permissions."""

    ADMIN = "admin"
    MANAGER = "manager"
    ENGINEER = "engineer"
    AUDITOR = "auditor"
    VIEWER = "viewer"


# Role hierarchy: higher index = more permissions
ROLE_HIERARCHY: dict[UserRole, int] = {
    UserRole.VIEWER: 0,
    UserRole.AUDITOR: 1,
    UserRole.ENGINEER: 2,
    UserRole.MANAGER: 3,
    UserRole.ADMIN: 4,
}


async def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> dict[str, Any]:
    """Extract and validate the current user from the Authorization header."""
    if settings.DEMO_MODE:
        # In demo mode, return a simulated admin user
        return {
            "sub": "demo-user-001",
            "role": "admin",
            "email": "demo@indusmind.ai",
            "full_name": "Demo User",
        }

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return decode_token(credentials.credentials)


def require_role(minimum_role: UserRole):
    """
    Dependency factory that enforces a minimum role.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role(UserRole.ADMIN))])
    """

    async def role_checker(
        payload: dict[str, Any] = Depends(get_current_user_payload),
    ) -> dict[str, Any]:
        user_role = UserRole(payload.get("role", "viewer"))
        if ROLE_HIERARCHY.get(user_role, 0) < ROLE_HIERARCHY[minimum_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {minimum_role.value} role or higher",
            )
        return payload

    return role_checker
