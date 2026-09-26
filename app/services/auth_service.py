"""Authentication service."""

from typing import Optional

from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.repositories.admin_repo import AdminRepository


class AuthService:
    """Handle authentication logic."""

    def __init__(self, admin_repo: AdminRepository) -> None:
        self.admin_repo = admin_repo

    async def authenticate(self, email: str, password: str) -> Optional[str]:
        """Authenticate admin and return JWT token."""
        admin = await self.admin_repo.find_by_email(email)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not verify_password(password, admin["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        token = create_access_token(data={"sub": admin["id"], "email": admin["email"]})
        return token

    async def get_current_admin(self, token: str) -> dict:
        """Validate token and return current admin."""
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        admin_id = payload.get("sub")
        if not admin_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        admin = await self.admin_repo.find_one_by_id(admin_id)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin not found",
            )

        return admin

    async def create_admin(self, email: str, password: str, full_name: str) -> dict:
        """Create a new admin user."""
        existing = await self.admin_repo.find_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin with this email already exists",
            )

        admin_data = {
            "email": email,
            "hashed_password": hash_password(password),
            "full_name": full_name,
            "is_active": True,
        }
        admin_id = await self.admin_repo.insert_one(admin_data)
        return await self.admin_repo.find_one_by_id(admin_id)
