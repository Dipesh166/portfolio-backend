"""FastAPI dependencies."""

from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.services.auth_service import AuthService
from app.repositories.admin_repo import AdminRepository


async def get_current_admin(
    authorization: Optional[str] = Header(None),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> dict:
    """Dependency to get authenticated admin user."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
        )

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Use: Bearer <token>",
        )

    token = parts[1]
    admin_repo = AdminRepository(database)
    auth_service = AuthService(admin_repo)
    return await auth_service.get_current_admin(token)
