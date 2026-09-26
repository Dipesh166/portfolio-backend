"""Music repository."""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.base import BaseRepository


class MusicRepository(BaseRepository):
    """Repository for music operations."""

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database["music"])

    async def get_all_ordered(self):
        """Get all music tracks sorted by display_order."""
        return await self.find_many(sort=[("display_order", 1)])

    async def get_enabled(self):
        """Get enabled music tracks sorted by display_order."""
        return await self.find_many(
            {"enabled": True}, sort=[("display_order", 1)]
        )