"""Achievement repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class AchievementRepository(BaseRepository):
    """Repository for achievement operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["achievements"])

    async def get_all_ordered(self):
        """Get all achievements sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])
