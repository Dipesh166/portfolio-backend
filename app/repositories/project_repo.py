"""Project repository."""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    """Repository for project operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["projects"])

    async def get_all_ordered(self):
        """Get all projects sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])

    async def get_featured(self):
        """Get featured projects."""
        return await self.find_many(
            query={"featured": True}, sort=[("display_order", 1)]
        )

    async def find_by_slug(self, slug: str) -> Optional[dict]:
        """Find a project by its slug."""
        return await self.find_one({"slug": slug})
