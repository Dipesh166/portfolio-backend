"""Admin repository."""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class AdminRepository(BaseRepository):
    """Repository for admin user operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["admins"])

    async def find_by_email(self, email: str) -> Optional[dict]:
        """Find admin by email address."""
        return await self.find_one({"email": email})
