"""Skill repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class SkillRepository(BaseRepository):
    """Repository for skill operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["skills"])

    async def get_all_ordered(self):
        """Get all skills sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])

    async def get_by_category(self, category: str):
        """Get skills filtered by category."""
        return await self.find_many(
            query={"category": category}, sort=[("display_order", 1)]
        )
