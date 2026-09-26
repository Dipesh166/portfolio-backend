"""Experience repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class ExperienceRepository(BaseRepository):
    """Repository for experience operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["experiences"])

    async def get_all_ordered(self):
        """Get all experiences sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])
